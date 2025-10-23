# core/reply_engine.py
import logging
import random
import google.generativeai as genai
from datetime import datetime
from config.templates import REPLY_TEMPLATES, emoji_map, AI_PROMPTS
from config.settings import GEMINI_API_KEY



class ReplyEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.history = set()  # 防止重复回复

        # 初始化表情符号映射
        self.emoji_map = emoji_map

        # 配置 Gemini
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            # 直接创建模型实例
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.logger.info("Gemini API 初始化成功")
        except Exception as e:
            self.logger.error(f"Gemini API 初始化失败: {str(e)}")
            raise

    def _generate_content(self, prompt, max_tokens=150, temperature=0.7):
        """统一的内容生成接口"""
        try:
            # 使用正确的生成方法
            response = self.model.generate_content(
                contents=prompt,
                generation_config={
                    'max_output_tokens': max_tokens,
                    'temperature': temperature
                }
            )

            if response.text:
                return response.text.strip()
            return None

        except Exception as e:
            self.logger.error(f"生成内容失败: {str(e)}")
            return None

    def _select_emoji(self, category):
        """选择合适的表情"""
        if category in self.emoji_map:
            return random.choice(self.emoji_map[category])
        return random.choice(self.emoji_map['general'])

    def generate_proactive_comment(self, video_data):
        """生成主动评论"""
        try:
            self.logger.info(f"正在为视频生成主动评论: {video_data.get('id', 'unknown')}")

            # 生成更自然的评论
            prompt = f"""
            请以观众的身份，对这个视频写一条友好的评论（50字以内）：

            视频描述：{video_data.get('description', '未知内容')}
            视频标题：{video_data.get('title', '未知标题')}

            要求：
            1. 用自然的口语表达
            2. 表达真诚的兴趣
            3. 可以提一个小问题或建议
            4. 避免过于专业或正式的语气
            """

            comment = self._generate_content(prompt, max_tokens=100, temperature=0.8)

            if comment:
                # 添加表情符号增加自然度
                emoji = self._select_emoji('positive')
                comment = f"{comment} {emoji}"
                self.logger.info("主动评论生成成功")
                return comment
            return None

        except Exception as e:
            self.logger.error(f"生成主动评论失败: {str(e)}")
            return None

    def _summarize_content(self, text):
        """使用更自然的方式总结内容"""
        try:
            self.logger.info("正在总结内容...")

            prompt = f"""
            作为一个普通观众，请用日常的口语简单说说这个内容主要讲了什么：

            {text}

            要求：
            1. 用简单的话概括
            2. 带有个人感受
            3. 不要太正式
            4. 50字以内
            """

            summary = self._generate_content(
                prompt,
                max_tokens=100,
                temperature=0.7
            )

            if summary:
                self.logger.info("内容总结完成")
                return summary
            return text[:50] + "..."

        except Exception as e:
            self.logger.error(f"内容总结失败: {str(e)}")
            return text[:50] + "..."

    def generate_mention_reply(self, mention_text, user_profile, video_context):
        """生成@提及回复"""
        try:
            prompt = self._create_mention_prompt(mention_text, user_profile, video_context)
            reply = self._generate_content(prompt, max_tokens=150, temperature=0.7)

            if reply:
                reply = self._add_interaction_hook(reply)
                return reply
            return self._get_fallback_reply()

        except Exception as e:
            self.logger.error(f"生成提及回复失败: {str(e)}")
            return self._get_fallback_reply()

    def _create_mention_prompt(self, mention_text, user_profile, video_context):
        """创建更自然的回复提示"""
        return f"""
        假设你是这个视频的创作者，请用朴实自然的语言回复这条评论：

        评论内容：{mention_text}

        背景信息：
        - 视频是关于：{video_context.get('title', '未知主题')}
        - 评论者感兴趣的话题：{', '.join(user_profile.get('interests', ['一般话题']))}

        要求：
        1. 用简单日常的口语回复
        2. 表达真诚的感谢
        3. 可以分享一点小故事或经验
        4. 鼓励继续交流
        5. 50字左右
        """

    def _get_fallback_reply(self):
        """获取后备回复"""
        replies = [
            "谢谢关注呀！你说得很有道理",
            "感谢留言！这个想法很棒诶",
            "收到你的评论啦，让我想了想",
            "谢谢分享！我也是这么觉得的",
        ]
        return f"{random.choice(replies)} {self._select_emoji('positive')}"

    def _add_interaction_hook(self, reply):
        """添加互动钩子"""
        hooks = [
            "你觉得呢？",
            "欢迎继续交流！",
            "期待你的想法~",
            "让我们一起探讨吧！"
        ]
        return f"{reply} {random.choice(hooks)} {self._select_emoji('positive')}"

    def _should_filter(self, text):
        """检查是否应该过滤回复"""
        return len(text) < 10 or text in self.history