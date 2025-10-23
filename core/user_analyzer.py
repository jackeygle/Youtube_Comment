# core/user_analyzer.py
import logging
from datetime import datetime, timedelta
import jieba.analyse
from snownlp import SnowNLP
from collections import defaultdict


class UserAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_data = defaultdict(lambda: {
            'comments': [],
            'emotions': [],
            'last_updated': None
        })
        self.cache_duration = timedelta(hours=24)

    def build_profile(self, user_id):
        """构建用户画像"""
        try:
            if not self._is_cache_valid(user_id):
                self._update_user_data(user_id)

            user = self.user_data[user_id]
            return {
                'top_interests': self._detect_interests(user_id),
                'emotion_stats': self._calculate_emotion(user_id),
                'activity_level': self._get_activity_level(user_id),
                'interaction_history': self._get_interaction_history(user_id)
            }
        except Exception as e:
            self.logger.error(f"Error building profile for user {user_id}: {str(e)}")
            return self._get_default_profile()

    def detect_emotion(self, text):
        """检测文本情感"""
        try:
            s = SnowNLP(text)
            score = s.sentiments

            if score > 0.7:
                return 'positive'
            elif score < 0.3:
                return 'negative'
            return 'neutral'

        except Exception as e:
            self.logger.error(f"Error detecting emotion: {str(e)}")
            return 'neutral'

    def _detect_interests(self, user_id):
        """分析用户兴趣"""
        try:
            texts = [c['text'] for c in self.user_data[user_id]['comments']]
            combined = ' '.join(texts)

            # 使用jieba提取关键词
            keywords = jieba.analyse.extract_tags(
                combined,
                topK=5,
                withWeight=True
            )

            return [{'keyword': k, 'weight': w} for k, w in keywords]

        except Exception as e:
            self.logger.error(f"Error detecting interests: {str(e)}")
            return []

    def _calculate_emotion(self, user_id):
        """计算情绪统计"""
        try:
            emotions = self.user_data[user_id]['emotions']
            if not emotions:
                return {
                    'positive_ratio': 0.5,
                    'recent_trend': 'neutral'
                }

            recent_emotions = emotions[-5:]
            positive_count = sum(1 for e in emotions if e > 0.6)

            return {
                'positive_ratio': positive_count / len(emotions),
                'recent_trend': self._detect_trend(recent_emotions)
            }

        except Exception as e:
            self.logger.error(f"Error calculating emotions: {str(e)}")
            return {'positive_ratio': 0.5, 'recent_trend': 'neutral'}

    def _detect_trend(self, scores):
        """检测情感趋势"""
        if not scores or len(scores) < 2:
            return 'neutral'

        trend = sum(scores[-2:]) / 2 - sum(scores[:-2]) / (len(scores) - 2)
        if trend > 0.1:
            return 'improving'
        elif trend < -0.1:
            return 'declining'
        return 'stable'

    def _get_activity_level(self, user_id):
        """获取活跃度"""
        try:
            comments = self.user_data[user_id]['comments']
            if not comments:
                return 'low'

            recent_comments = [c for c in comments
                               if datetime.fromisoformat(c['timestamp']) >
                               datetime.utcnow() - timedelta(days=7)]

            count = len(recent_comments)
            if count > 10:
                return 'high'
            elif count > 5:
                return 'medium'
            return 'low'

        except Exception as e:
            self.logger.error(f"Error getting activity level: {str(e)}")
            return 'low'

    def _is_cache_valid(self, user_id):
        """检查缓存是否有效"""
        if user_id not in self.user_data:
            return False

        last_updated = self.user_data[user_id]['last_updated']
        if not last_updated:
            return False

        return datetime.utcnow() - last_updated < self.cache_duration

    def _update_user_data(self, user_id):
        """更新用户数据"""
        # 实际实现中，这里应该从YouTube API获取用户的历史评论等数据
        self.user_data[user_id]['last_updated'] = datetime.utcnow()

    def _get_default_profile(self):
        """返回默认用户画像"""
        return {
            'top_interests': [],
            'emotion_stats': {'positive_ratio': 0.5, 'recent_trend': 'neutral'},
            'activity_level': 'low',
            'interaction_history': []
        }

    def _get_interaction_history(self, user_id):
        """获取互动历史"""
        return self.user_data[user_id]['comments'][-5:]