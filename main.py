# main.py
import os
import logging
import schedule
import time
from datetime import datetime
from core.youtube_service import YouTubeService
from core.video_discover import VideoDiscover
from core.comment_monitor import CommentMonitor
from core.mention_handler import MentionHandler
from core.user_analyzer import UserAnalyzer
from core.reply_engine import ReplyEngine
from core.safety_checker import SafetyChecker
from config.settings import setup_logging


class MainController:
    def __init__(self):
        # 初始化日志
        setup_logging()
        self.logger = logging.getLogger(__name__)

        try:
            # 显示启动信息
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            self.logger.info(f"\n{'=' * 50}")
            self.logger.info(f"系统启动")
            self.logger.info(f"时间: {current_time}")
            self.logger.info(f"用户: {os.getenv('USER', 'woainio15200')}")
            self.logger.info(f"{'=' * 50}\n")

            # 初始化组件
            self.logger.info("初始化 YouTube 服务...")
            self.youtube = YouTubeService()

            self.logger.info("初始化核心组件...")
            self.discover = VideoDiscover(self.youtube)
            self.monitor = CommentMonitor(self.youtube)
            self.mentions = MentionHandler(self.youtube)
            self.analyzer = UserAnalyzer()
            self.reply = ReplyEngine()
            self.safety = SafetyChecker()

            # 设置定时任务
            self.logger.info("配置定时任务...")
            schedule.every(1).minutes.do(self._handle_proactive_comments)  # 每分钟执行一次
            schedule.every(2).minutes.do(self._handle_incoming_comments)
            schedule.every(1).hours.do(self._cleanup)

            self.logger.info("初始化完成")
        except Exception as e:
            self.logger.error(f"初始化失败: {str(e)}")
            raise

    def post_comment(self, video_id, comment_text):
        """发布评论的统一接口"""
        try:
            self.logger.info(f"准备发布评论到视频 {video_id}")
            self.logger.info(f"评论内容: {comment_text[:100]}..." if len(comment_text) > 100 else comment_text)

            response = self.youtube.service.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": video_id,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": comment_text
                            }
                        }
                    }
                }
            ).execute()

            self.monitor.add_comment_record(video_id)
            self.logger.info("评论发布成功")
            return response
        except Exception as e:
            self.logger.error(f"发布评论失败: {str(e)}")
            return None

    def _handle_proactive_comments(self):
        """处理主动评论任务"""
        try:
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            self.logger.info(f"\n{'=' * 50}")
            self.logger.info(f"开始新一轮视频查找和评论 - {current_time}")
            self.logger.info(f"{'=' * 50}")

            new_videos = self.discover.find_target_videos()
            self.logger.info(f"找到 {len(new_videos)} 个新视频")

            for idx, video in enumerate(new_videos[:3], 1):
                video_id = video.get('id', 'unknown')
                title = video.get('snippet', {}).get('title', 'unknown')

                self.logger.info(f"\n处理第 {idx} 个视频:")
                self.logger.info(f"视频ID: {video_id}")
                self.logger.info(f"标题: {title}")

                if not self.monitor.has_commented(video_id):
                    try:
                        self.logger.info("生成评论中...")
                        comment = self.reply.generate_proactive_comment(video)

                        self.logger.info("检查评论安全性...")
                        if self.safety.check(comment):
                            response = self.post_comment(video_id, comment)
                            if response:
                                self.logger.info(f"成功评论视频 {video_id}")
                        else:
                            self.logger.warning("评论未通过安全检查")
                    except Exception as e:
                        self.logger.error(f"处理视频 {video_id} 时出错: {str(e)}")
                        continue
                else:
                    self.logger.info(f"视频 {video_id} 已评论过，跳过")

        except Exception as e:
            self.logger.error(f"视频查找评论任务出错: {str(e)}")

    def _handle_incoming_comments(self):
        """处理收到的评论"""
        try:
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            self.logger.info(f"\n处理新收到的评论 - {current_time}")

            new_comments = self.monitor.get_new_comments()
            self.logger.info(f"发现 {len(new_comments)} 条新评论")

            for comment in new_comments:
                try:
                    comment_id = comment.get('id', 'unknown')
                    self.logger.info(f"\n处理评论 ID: {comment_id}")

                    if self.mentions.is_mention(comment):
                        self.logger.info("检测到提及，处理提及评论...")
                        self._handle_mention(comment)
                    else:
                        self.logger.info("处理普通评论...")
                        self._handle_normal_comment(comment)
                except Exception as e:
                    self.logger.error(f"处理评论 {comment_id} 时出错: {str(e)}")
                    continue
        except Exception as e:
            self.logger.error(f"处理新评论任务出错: {str(e)}")

    def _handle_mention(self, comment):
        """处理提及评论"""
        try:
            comment_id = comment.get('id', 'unknown')
            self.logger.info(f"分析用户资料...")
            user_profile = self.analyzer.build_profile(comment['author'])

            self.logger.info(f"获取视频上下文...")
            video_context = self.mentions.get_video_context(comment['videoId'])

            if not video_context:
                self.logger.warning(f"无法获取视频 {comment['videoId']} 的上下文")
                return

            self.logger.info("生成回复...")
            reply = self.reply.generate_mention_reply(
                comment['text'],
                user_profile,
                video_context
            )

            if self.safety.check(reply):
                self.monitor.post_reply(comment_id, reply)
                self.logger.info(f"成功回复提及评论 {comment_id}")
            else:
                self.logger.warning("回复未通过安全检查")
        except Exception as e:
            self.logger.error(f"处理提及评论出错: {str(e)}")

    def _handle_normal_comment(self, comment):
        """处理普通评论"""
        try:
            comment_id = comment.get('id', 'unknown')
            self.logger.info("分析评论情感...")
            emotion = self.analyzer.detect_emotion(comment['text'])

            self.logger.info("生成自动回复...")
            reply = self.reply.generate_auto_reply(emotion)

            if self.safety.check(reply):
                self.monitor.post_reply(comment_id, reply)
                self.logger.info(f"成功回复评论 {comment_id}")
            else:
                self.logger.warning("回复未通过安全检查")
        except Exception as e:
            self.logger.error(f"处理普通评论出错: {str(e)}")

    def _cleanup(self):
        """清理过期数据"""
        try:
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            self.logger.info(f"\n开始清理过期数据 - {current_time}")

            self.monitor.cleanup_old_records()
            self.mentions.cleanup_cache()
            self.logger.info("数据清理完成")
        except Exception as e:
            self.logger.error(f"数据清理出错: {str(e)}")

    def run(self):
        """运行主循环"""
        self.logger.info("YouTube Bot 启动...")
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("\n收到停止信号，正在关闭程序...")
                break
            except Exception as e:
                self.logger.error(f"主循环出错: {str(e)}")
                self.logger.info("5秒后重试...")
                time.sleep(5)


if __name__ == "__main__":
    try:
        controller = MainController()
        controller.run()
    except Exception as e:
        logging.error(f"程序终止: {str(e)}")