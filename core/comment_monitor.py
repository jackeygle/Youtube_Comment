# core/comment_monitor.py
import logging
from datetime import datetime, timedelta
from config.settings import CHANNEL_ID


class CommentMonitor:
    def __init__(self, youtube_service):
        self.logger = logging.getLogger(__name__)
        self.youtube = youtube_service
        self.last_check_time = None
        self.processed_comments = set()
        self.commented_videos = {}  # 添加这个属性来跟踪已评论的视频

    def has_commented(self, video_id):
        """检查是否已经对视频进行了评论"""
        return video_id in self.commented_videos

    def add_comment_record(self, video_id):
        """记录已评论的视频"""
        self.commented_videos[video_id] = datetime.utcnow()

    def cleanup_old_records(self):
        """清理旧的评论记录"""
        try:
            current_time = datetime.utcnow()
            expired_videos = []

            # 清理超过7天的记录
            for video_id, comment_time in self.commented_videos.items():
                if current_time - comment_time > timedelta(days=7):
                    expired_videos.append(video_id)

            # 删除过期记录
            for video_id in expired_videos:
                del self.commented_videos[video_id]

            if expired_videos:
                self.logger.info(f"Cleaned up {len(expired_videos)} old comment records")

        except Exception as e:
            self.logger.error(f"Error cleaning up old records: {str(e)}")

    def get_new_comments(self):
        """获取新评论"""
        try:
            request = self.youtube.service.commentThreads().list(
                part='snippet',
                maxResults=100,
                order='time',
                textFormat='plainText',
                allThreadsRelatedToChannelId=CHANNEL_ID
            )

            response = self.youtube.execute_with_retry(request)

            if 'items' not in response:
                self.logger.warning("No comments found")
                return []

            current_time = datetime.utcnow()
            new_comments = []

            for item in response['items']:
                comment_id = item['id']

                # 跳过已处理的评论
                if comment_id in self.processed_comments:
                    continue

                comment = item['snippet']['topLevelComment']['snippet']
                comment_time = datetime.strptime(
                    comment['publishedAt'],
                    '%Y-%m-%dT%H:%M:%SZ'
                )

                # 只处理最近24小时内的评论
                if current_time - comment_time <= timedelta(hours=24):
                    new_comments.append({
                        'id': comment_id,
                        'text': comment['textDisplay'],
                        'author': comment['authorDisplayName'],
                        'publishedAt': comment['publishedAt'],
                        'videoId': item['snippet']['videoId']
                    })
                    self.processed_comments.add(comment_id)

            self.last_check_time = current_time
            return new_comments

        except Exception as e:
            self.logger.error(f"Error getting new comments: {str(e)}")
            return []