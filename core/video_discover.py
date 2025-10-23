# core/video_discover.py
import logging
from datetime import datetime, timedelta
# from .youtube_service import YouTubeService

class VideoDiscover:
    def __init__(self, youtube_service):
        self.logger = logging.getLogger(__name__)
        self.youtube = youtube_service
        self.last_checked = datetime.utcnow() - timedelta(hours=1)
        self.BLACKLIST = set()  # Channel blacklist
        self.processed_videos = set()  # Processed video set

    def find_target_videos(self, query_terms=['technology', 'programming', 'AI'], max_results=20):
        """Find target videos"""
        try:
            query = '|'.join(query_terms)
            search_request = self.youtube.service.search().list(
                part='snippet',
                q=query,
                type='video',
                publishedAfter=(self.last_checked - timedelta(hours=1)).isoformat() + 'Z',
                maxResults=max_results,
                relevanceLanguage='zh',
                safeSearch='moderate'
            )

            search_response = self.youtube.execute_with_retry(search_request)
            valid_videos = []

            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                if (video_id not in self.processed_videos and
                        self._is_valid_video(item)):
                    video_data = self._extract_video_data(item)
                    valid_videos.append(video_data)
                    self.processed_videos.add(video_id)

            self.last_checked = datetime.utcnow()
            self.logger.info(f"Found {len(valid_videos)} new valid videos")
            return valid_videos

        except Exception as e:
            self.logger.error(f"Error in find_target_videos: {str(e)}")
            return []

    def _is_valid_video(self, video_item):
        """Validate video eligibility"""
        try:
            snippet = video_item['snippet']
            channel_id = snippet['channelId']
            title = snippet['title'].lower()
            description = snippet['description'].lower()

            # Check blacklist
            if channel_id in self.BLACKLIST:
                return False

            # Ad keywords check
            ad_keywords = ['ad', 'sponsored', 'promotion', 'ad:']
            if any(keyword in title for keyword in ad_keywords):
                return False

            # Target keywords check
            target_keywords = [
                'tutorial', 'howto', 'analysis',
                'review', 'technology', 'programming', 'AI'
            ]
            has_target_keyword = any(
                keyword in title or keyword in description
                for keyword in target_keywords
            )

            return has_target_keyword

        except Exception as e:
            self.logger.error(f"Error in _is_valid_video: {str(e)}")
            return False

    def _extract_video_data(self, video_item):
        """Extract video metadata"""
        snippet = video_item['snippet']
        return {
            'id': video_item['id']['videoId'],
            'title': snippet['title'],
            'description': snippet['description'],
            'channelId': snippet['channelId'],
            'channelTitle': snippet['channelTitle'],
            'publishedAt': snippet['publishedAt'],
            'thumbnails': snippet['thumbnails']
        }

    def get_video_stats(self, video_id):
        """Get video statistics"""
        try:
            video_response = self.youtube.get_video_details(video_id)
            if video_response:
                return video_response['statistics']
            return None
        except Exception as e:
            self.logger.error(f"Error getting video stats: {str(e)}")
            return None