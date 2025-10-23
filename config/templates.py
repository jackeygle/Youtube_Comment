# config/templates.py
# Emoji Configuration
emoji_map = {
    'tech': ['(=^･ω･^=)', 'ฅ(≧ω≦)ฅ', '(｀・ω・´)', '(=^･^=)'],
    'emotional': ['(っ´▽`)っ', '(=´ω`=)', '(｡♥‿♥｡)', '(｀･ω･´)ゞ'],
    'general': ['ฅ^•ﻌ•^ฅ', '(=ↀωↀ=)✧', '(●´ω｀●)', '(◕‿◕✿)'],
    'positive': ['(｡♥‿♥｡)', '(●´∀｀●)', '(◠‿◠✿)', '٩(◕‿◕｡)۶'],
    'negative': ['(´･_･`)', '(っ´ω｀c)', '(╥﹏╥)', '(´;ω;｀)']
}

# Reply Templates
REPLY_TEMPLATES = {
    'proactive': [
        "ฅ^•ﻌ•^ฅ The {summary} mentioned in the video is interesting! What does everyone think? {emoji}",
        "Regarding {summary}, I have some questions to discuss~ {emoji}",
        "This perspective on {summary} is quite unique! Want to hear everyone's thoughts {emoji}",
        "Sharing my views on {summary}... {emoji}"
    ],
    'positive': [
        "Great idea! {emoji}",
        "Completely agree with your point~ {emoji}",
        "Well said! {emoji}",
        "Your perspective is very insightful {emoji}"
    ],
    'negative': [
        "Sending virtual hugs~ {emoji}",
        "Everything will be okay {emoji}",
        "Let's cheer up together! {emoji}",
        "Believe tomorrow will be better {emoji}"
    ],
    'neutral': [
        "Thanks for sharing your thoughts {emoji}",
        "This perspective is interesting {emoji}",
        "Let's explore this topic together {emoji}",
        "Looking forward to more discussions {emoji}"
    ]
}

# AI Prompt Templates
AI_PROMPTS = {
    'comment_analysis': """
    Analyze the emotional tone and key points of the following comment:
    Comment content: {comment_text}
    Please consider:
    1. Overall sentiment (positive/negative/neutral)
    2. Main points
    3. Whether response is needed
    """,

    'response_generation': """
    Generate a natural, friendly response considering:
    1. User comment: {comment}
    2. User interests: {interests}
    3. Interaction history: {history}
    4. Response tone: {tone}
    Requirements:
    - Maintain friendliness and professionalism
    - Keep it natural and authentic
    - Use emojis appropriately
    """
}