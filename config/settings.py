# config/settings.py
import os
import logging
from datetime import datetime

# 基础配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# API 密钥配置（默认从环境变量读取，实际值在 settings_local.py 中）
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# YouTube API Service Account 配置
# OAuth 2.0 客户端凭证路径
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'credentials', 'credentials.json')
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# YouTube API 作用域
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# 频道配置
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID', '')  # 实际值在 settings_local.py 中

# OpenAI配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# 日志配置
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'youtube_bot.log')


def setup_logging():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )


# API速率限制配置
RATE_LIMITS = {
    'comments_per_hour': 15,
    'mentions_priority': 5,
    'max_retries': 3,
    'retry_delay': 60  # seconds
}

# 数据清理配置
CLEANUP_CONFIG = {
    'max_age_days': 7,
    'batch_size': 100
}

# 导入本地配置（如果存在）
# settings_local.py 包含实际的 API 密钥，不会上传到 Git
try:
    from .settings_local import *
except ImportError:
    pass  # 如果没有 settings_local.py，使用环境变量