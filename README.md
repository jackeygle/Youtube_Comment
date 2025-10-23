# YouTube Comment Bot 🤖

一个智能化的 YouTube 评论自动化机器人，基于 Google Gemini AI 生成自然、友好的评论和回复。

## ✨ 主要功能

- **🎯 智能视频发现**：自动发现符合条件的新视频
- **💬 自动评论生成**：使用 Gemini AI 生成自然、个性化的评论
- **📬 评论监控**：实时监控收到的评论和@提及
- **🔄 智能回复**：根据评论内容和用户画像生成合适的回复
- **👤 用户分析**：分析用户兴趣和行为模式
- **🛡️ 安全检查**：确保评论内容符合 YouTube 社区准则
- **⏱️ 定时任务**：自动化运行，无需人工干预

## 🏗️ 项目结构

```
YouTubecomment/
├── config/                 # 配置文件
│   ├── settings.py        # 系统配置
│   └── templates.py       # 评论模板
├── core/                   # 核心功能模块
│   ├── comment_monitor.py # 评论监控
│   ├── mention_handler.py # @提及处理
│   ├── reply_engine.py    # 回复生成引擎
│   ├── safety_checker.py  # 安全检查
│   ├── user_analyzer.py   # 用户分析
│   ├── video_discover.py  # 视频发现
│   └── youtube_service.py # YouTube API 服务
├── credentials/            # API 凭证（不上传到 Git）
├── logs/                   # 日志文件
├── main.py                 # 主程序入口
└── README.md               # 项目说明
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- Google Cloud Platform 账号
- YouTube Data API v3 访问权限
- Google Gemini API Key

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API 凭证

#### YouTube API 设置

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 YouTube Data API v3
4. 创建 OAuth 2.0 客户端 ID
5. 下载凭证文件并保存为 `credentials/credentials.json`

#### Gemini API 设置

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建 API Key
3. 在 `config/settings.py` 中配置或使用环境变量

### 4. 配置频道信息

在 `config/settings.py` 中修改以下配置：

```python
CHANNEL_ID = 'YOUR_CHANNEL_ID'  # 替换为你的频道 ID
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'  # 建议使用环境变量
```

### 5. 运行程序

```bash
python main.py
```

## ⚙️ 配置说明

### API 速率限制

在 `config/settings.py` 中配置：

```python
RATE_LIMITS = {
    'comments_per_hour': 15,      # 每小时评论数量限制
    'mentions_priority': 5,       # @提及优先级
    'max_retries': 3,             # 最大重试次数
    'retry_delay': 60             # 重试延迟（秒）
}
```

### 定时任务

默认定时任务配置：

- 主动评论：每 1 分钟检查一次新视频
- 回复评论：每 2 分钟检查一次新评论
- 数据清理：每 1 小时清理一次过期数据

可在 `main.py` 的 `MainController.__init__()` 中修改。

## 🔒 安全建议

⚠️ **重要提示**：

1. **不要**将 API 密钥直接提交到代码库
2. 使用环境变量或密钥管理服务存储敏感信息
3. 将 `credentials/` 和 `.env` 添加到 `.gitignore`
4. 定期轮换 API 密钥
5. 遵守 YouTube 服务条款和社区准则

### 使用环境变量（推荐）

```bash
export GEMINI_API_KEY="your_gemini_api_key"
export OPENAI_API_KEY="your_openai_api_key"  # 如果使用
```

## 📊 日志

所有运行日志保存在 `logs/youtube_bot.log`，包括：

- 系统启动信息
- 视频发现记录
- 评论发布记录
- 回复处理记录
- 错误和异常信息

## 🛠️ 技术栈

- **Python 3.8+**
- **Google YouTube Data API v3** - YouTube 数据操作
- **Google Gemini AI** - 智能评论生成
- **schedule** - 定时任务调度
- **logging** - 日志记录

## 📝 功能详解

### 视频发现 (VideoDiscover)

自动搜索和筛选目标视频，支持：
- 关键词搜索
- 时间范围过滤
- 播放量筛选
- 避免重复评论

### 评论生成 (ReplyEngine)

使用 Gemini AI 生成评论，特点：
- 自然的口语化表达
- 根据视频内容定制
- 添加合适的表情符号
- 避免重复内容

### 用户分析 (UserAnalyzer)

分析用户行为和兴趣：
- 评论历史分析
- 兴趣标签提取
- 情感检测
- 个性化回复

## ⚠️ 注意事项

1. **遵守 YouTube 政策**：确保所有操作符合 YouTube 服务条款
2. **速率限制**：合理设置评论频率，避免被识别为垃圾评论
3. **内容质量**：生成的评论应该有价值，避免无意义的刷屏
4. **隐私保护**：不收集或存储用户个人信息
5. **监控运行**：定期检查日志，确保程序正常运行

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

- GitHub: [@jackeygle](https://github.com/jackeygle)

## 🔗 相关资源

- [YouTube Data API 文档](https://developers.google.com/youtube/v3)
- [Google Gemini API 文档](https://ai.google.dev/docs)
- [YouTube 社区准则](https://www.youtube.com/howyoutubeworks/policies/community-guidelines/)

---

**免责声明**：本项目仅供学习和研究使用。使用本项目进行任何自动化操作前，请确保遵守 YouTube 的服务条款和相关法律法规。开发者不对使用本项目造成的任何后果负责。

