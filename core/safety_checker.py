# core/safety_checker.py
import logging
import re
from collections import defaultdict
from datetime import datetime, timedelta


class SafetyChecker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.forbidden_words = set([
            # 添加需要过滤的违禁词
        ])
        self.spam_patterns = [
            r'(https?://\S+)',
            r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'([\+]?\d{11,})',
        ]
        self.rate_limits = defaultdict(list)
        self.max_comments_per_hour = 15

    def check(self, text, user_id=None):
        """检查内容是否安全"""
        try:
            if not text:
                return False

            checks = [
                self._check_forbidden_words(text),
                self._check_spam(text),
                self._check_length(text)
            ]

            if user_id:
                checks.append(self._check_rate_limit(user_id))

            return all(checks)

        except Exception as e:
            self.logger.error(f"Error in safety check: {str(e)}")
            return False

    def _check_forbidden_words(self, text):
        """检查违禁词"""
        text_lower = text.lower()
        for word in self.forbidden_words:
            if word in text_lower:
                self.logger.warning(f"Found forbidden word: {word}")
                return False
        return True

    def _check_spam(self, text):
        """检查垃圾信息"""
        for pattern in self.spam_patterns:
            if re.search(pattern, text):
                self.logger.warning(f"Detected spam pattern in text")
                return False
        return True

    def _check_length(self, text):
        """检查文本长度"""
        text_length = len(text)
        if text_length < 2 or text_length > 1000:
            self.logger.warning(f"Text length ({text_length}) out of bounds")
            return False
        return True

    def _check_rate_limit(self, user_id):
        """检查频率限制"""
        current_time = datetime.utcnow()
        hour_ago = current_time - timedelta(hours=1)

        # 清理旧的记录
        self.rate_limits[user_id] = [
            t for t in self.rate_limits[user_id]
            if t > hour_ago
        ]

        # 检查频率
        if len(self.rate_limits[user_id]) >= self.max_comments_per_hour:
            self.logger.warning(f"Rate limit exceeded for user {user_id}")
            return False

        self.rate_limits[user_id].append(current_time)
        return True

    def add_forbidden_word(self, word):
        """添加违禁词"""
        self.forbidden_words.add(word.lower())

    def remove_forbidden_word(self, word):
        """移除违禁词"""
        self.forbidden_words.discard(word.lower())

    def update_spam_patterns(self, patterns):
        """更新垃圾信息模式"""
        try:
            for pattern in patterns:
                re.compile(pattern)  # 验证正则表达式是否有效
            self.spam_patterns.extend(patterns)
        except Exception as e:
            self.logger.error(f"Invalid spam pattern: {str(e)}")

    def cleanup(self):
        """清理过期数据"""
        current_time = datetime.utcnow()
        expired_users = []

        for user_id, timestamps in self.rate_limits.items():
            if all(t < current_time - timedelta(hours=24) for t in timestamps):
                expired_users.append(user_id)

        for user_id in expired_users:
            del self.rate_limits[user_id]