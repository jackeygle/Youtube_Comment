# YouTube Comment Bot 🤖

An intelligent YouTube comment automation bot powered by Google Gemini AI to generate natural, friendly comments and replies.

## ✨ Key Features

- **🎯 Smart Video Discovery**: Automatically discover target videos matching your criteria
- **💬 Intelligent Comment Generation**: Generate natural, personalized comments using Gemini AI
- **📬 Comment Monitoring**: Real-time monitoring of received comments and @mentions
- **🔄 Smart Replies**: Generate contextual replies based on comment content and user profiles
- **👤 User Analysis**: Analyze user interests and behavioral patterns
- **🛡️ Safety Checker**: Ensure all comments comply with YouTube community guidelines
- **⏱️ Scheduled Tasks**: Fully automated operation with no manual intervention required

## 🏗️ Project Structure

```
YouTubecomment/
├── config/                 # Configuration files
│   ├── settings.py        # System configuration
│   └── templates.py       # Comment templates
├── core/                   # Core functionality modules
│   ├── comment_monitor.py # Comment monitoring
│   ├── mention_handler.py # @mention processing
│   ├── reply_engine.py    # Reply generation engine
│   ├── safety_checker.py  # Safety validation
│   ├── user_analyzer.py   # User analysis
│   ├── video_discover.py  # Video discovery
│   └── youtube_service.py # YouTube API service
├── credentials/            # API credentials (not uploaded to Git)
├── logs/                   # Log files
├── main.py                 # Main program entry point
└── README.md               # Project documentation
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Google Cloud Platform account
- YouTube Data API v3 access
- Google Gemini API Key

### 2. Installation

```bash
pip install -r requirements.txt
```

### 3. API Credentials Setup

#### YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable YouTube Data API v3
4. Create OAuth 2.0 Client ID credentials
5. Download credentials file and save as `credentials/credentials.json`

#### Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API Key
3. Configure in `config/settings.py` or use environment variables

### 4. Configuration

Create `config/settings_local.py` with your actual credentials:

```python
# config/settings_local.py
GEMINI_API_KEY = "your_gemini_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"  # Optional
CHANNEL_ID = "your_youtube_channel_id_here"
```

### 5. Run the Bot

```bash
python main.py
```

## ⚙️ Configuration

### API Rate Limits

Configure in `config/settings.py`:

```python
RATE_LIMITS = {
    'comments_per_hour': 15,      # Maximum comments per hour
    'mentions_priority': 5,       # Priority for @mentions
    'max_retries': 3,             # Maximum retry attempts
    'retry_delay': 60             # Retry delay in seconds
}
```

### Scheduled Tasks

Default task schedule:

- Proactive commenting: Check for new videos every 1 minute
- Reply to comments: Check for new comments every 2 minutes
- Data cleanup: Clean expired data every 1 hour

You can modify these in `main.py` within the `MainController.__init__()` method.

## 🔒 Security Best Practices

⚠️ **Important**:

1. **Never** commit API keys directly to your repository
2. Use environment variables or local configuration files for sensitive data
3. Add `credentials/` and `.env` to `.gitignore`
4. Rotate API keys regularly
5. Comply with YouTube Terms of Service and Community Guidelines

### Using Environment Variables (Recommended)

```bash
export GEMINI_API_KEY="your_gemini_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export YOUTUBE_CHANNEL_ID="your_channel_id"
```

## 📊 Logging

All operational logs are saved in `logs/youtube_bot.log`, including:

- System startup information
- Video discovery records
- Comment posting records
- Reply processing records
- Errors and exceptions

## 🛠️ Technology Stack

- **Python 3.8+**
- **Google YouTube Data API v3** - YouTube data operations
- **Google Gemini AI** - Intelligent comment generation
- **schedule** - Task scheduling
- **logging** - Log management

## 📝 Feature Details

### Video Discovery (VideoDiscover)

Automatically search and filter target videos with support for:
- Keyword searching
- Time range filtering
- View count filtering
- Duplicate comment prevention

### Comment Generation (ReplyEngine)

Generate comments using Gemini AI with features:
- Natural conversational expression
- Content customized to video context
- Appropriate emoji usage
- Duplicate content avoidance

### User Analysis (UserAnalyzer)

Analyze user behavior and interests:
- Comment history analysis
- Interest tag extraction
- Sentiment detection
- Personalized replies

## ⚠️ Important Notes

1. **Comply with YouTube Policies**: Ensure all operations comply with YouTube Terms of Service
2. **Rate Limiting**: Set reasonable comment frequencies to avoid spam detection
3. **Content Quality**: Generated comments should be valuable and avoid meaningless spam
4. **Privacy Protection**: Do not collect or store personal user information
5. **Monitor Operations**: Regularly check logs to ensure proper functioning

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License

## 👨‍💻 Author

- GitHub: [@jackeygle](https://github.com/jackeygle)

## 🔗 Related Resources

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [YouTube Community Guidelines](https://www.youtube.com/howyoutubeworks/policies/community-guidelines/)

---

**Disclaimer**: This project is for educational and research purposes only. Before using this project for any automated operations, please ensure compliance with YouTube's Terms of Service and applicable laws. The developer is not responsible for any consequences arising from the use of this project.
