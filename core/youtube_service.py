import os
import logging
import time
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config.settings import (
    SCOPES,
    CLIENT_SECRET_FILE,
    API_SERVICE_NAME,
    API_VERSION,
    RATE_LIMITS,
    CHANNEL_ID
)

class YouTubeService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.credentials = self._get_oauth_credentials()
        self.service = build(API_SERVICE_NAME, API_VERSION, credentials=self.credentials)
        self._request_count = 0
        self._last_request_time = time.time()

    def _get_oauth_credentials(self):
        """获取 OAuth 2.0 凭证"""
        credentials = None
        # 如果有保存的凭证，则加载它
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        # 如果没有凭证或凭证无效，重新进行 OAuth 认证
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, SCOPES)
                credentials = flow.run_local_server(port=0)

            # 保存凭证，以便下次使用
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    def _handle_rate_limit(self):
        """处理API请求速率限制"""
        current_time = time.time()
        if current_time - self._last_request_time < 1:
            time.sleep(1)
        self._last_request_time = current_time
        self._request_count += 1

    def execute_with_retry(self, request, max_retries=RATE_LIMITS['max_retries']):
        """执行API请求，带重试机制"""
        for attempt in range(max_retries):
            try:
                self._handle_rate_limit()
                return request.execute()
            except HttpError as e:
                if e.resp.status in [429, 500, 503]:  # Rate limit or server error
                    if attempt == max_retries - 1:
                        raise
                    wait_time = (attempt + 1) * RATE_LIMITS['retry_delay']
                    self.logger.warning(f"API request failed, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise

    def get_video_details(self, video_id):
        """获取视频详细信息"""
        try:
            request = self.service.videos().list(
                part='snippet,statistics',
                id=video_id
            )
            response = self.execute_with_retry(request)
            if response['items']:
                return response['items'][0]
            return None
        except Exception as e:
            self.logger.error(f"Error getting video details: {str(e)}")
            return None

    def get_channel_info(self):
        """获取频道信息"""
        try:
            request = self.service.channels().list(
                part="snippet,statistics",
                id=CHANNEL_ID
            )
            response = self.execute_with_retry(request)
            if response['items']:
                return response['items'][0]
            return None
        except Exception as e:
            self.logger.error(f"Error getting channel info: {str(e)}")
            return None

    def test_connection(self):
        """测试API连接"""
        try:
            channel_info = self.get_channel_info()
            if channel_info:
                self.logger.info(f"Successfully connected to channel: {channel_info['snippet']['title']}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False