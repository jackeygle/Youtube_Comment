# core/mention_handler.py
import logging
from datetime import datetime, timedelta
from config.settings import CHANNEL_ID  # 添加这行导入


class MentionHandler:
    def __init__(self, youtube_service):
        self.logger = logging.getLogger(__name__)
        self.youtube = youtube_service
        self.channel_info = None
        self.mention_cache = {}  # 缓存提及信息
        self._load_channel_info()

    def _load_channel_info(self):
        """加载频道信息"""
        try:
            # 使用 CHANNEL_ID 而不是 mine=True
            request = self.youtube.service.channels().list(
                part='snippet',
                id=CHANNEL_ID  # 修改这里
            )
            response = self.youtube.execute_with_retry(request)
            if 'items' in response and response['items']:
                self.channel_info = response['items'][0]['snippet']
                self.logger.info(f"Channel info loaded successfully for channel: {self.channel_info['title']}")
            else:
                self.logger.error("No channel information found")
                self.channel_info = None
        except Exception as e:
            self.logger.error(f"Error loading channel info: {str(e)}")
            self.channel_info = None

    def is_mention(self, comment):
        """检查评论是否包含@提及"""
        if not self.channel_info:
            self.logger.warning("Channel info not available, retrying to load")
            self._load_channel_info()
            if not self.channel_info:
                return False

        text = comment.get('text', '').lower()
        channel_name = self.channel_info['title'].lower()

        # 检查直接@提及或频道名称提及
        return f'@{channel_name}' in text or channel_name in text

    def get_video_context(self, video_id):
        """获取视频上下文信息"""
        try:
            # 检查缓存
            if video_id in self.mention_cache:
                return self.mention_cache[video_id]

            video_response = self.youtube.get_video_details(video_id)
            if video_response and 'snippet' in video_response:
                context = {
                    'title': video_response['snippet'].get('title', ''),
                    'description': video_response['snippet'].get('description', ''),
                    'tags': video_response['snippet'].get('tags', []),
                    'publishedAt': video_response['snippet'].get('publishedAt', ''),
                    'viewCount': video_response.get('statistics', {}).get('viewCount', 0),
                    'likeCount': video_response.get('statistics', {}).get('likeCount', 0)
                }
                self.mention_cache[video_id] = context
                return context

            self.logger.warning(f"No video details found for video ID: {video_id}")
            return None

        except Exception as e:
            self.logger.error(f"Error getting video context for video {video_id}: {str(e)}")
            return None

    def cleanup_cache(self):
        """清理过期缓存"""
        try:
            current_time = datetime.utcnow()
            expired_ids = []

            for video_id, cache_data in self.mention_cache.items():
                if 'publishedAt' not in cache_data:
                    expired_ids.append(video_id)
                    continue

                try:
                    cache_time = datetime.fromisoformat(
                        cache_data['publishedAt'].replace('Z', '+00:00')
                    )
                    if current_time - cache_time > timedelta(days=7):
                        expired_ids.append(video_id)
                except (ValueError, TypeError) as e:
                    self.logger.error(f"Error parsing date for video {video_id}: {str(e)}")
                    expired_ids.append(video_id)

            for video_id in expired_ids:
                del self.mention_cache[video_id]

            if expired_ids:
                self.logger.info(f"Cleaned up {len(expired_ids)} cached items")

        except Exception as e:
            self.logger.error(f"Error during cache cleanup: {str(e)}")