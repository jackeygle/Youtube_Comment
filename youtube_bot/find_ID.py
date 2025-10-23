from googleapiclient.discovery import build
from google.oauth2 import service_account


def get_channel_id():
    # 初始化认证
    credentials = service_account.Credentials.from_service_account_file(
        '/credentials/account_service.json',
        scopes=['https://www.googleapis.com/auth/youtube.readonly']
    )

    # 创建 YouTube API 客户端
    youtube = build('youtube', 'v3', credentials=credentials)

    # 获取自己的频道信息
    request = youtube.channels().list(
        part="id",
        mine=True
    )
    response = request.execute()

    if 'items' in response:
        channel_id = response['items'][0]['id']
        print(f"Your channel ID is: {channel_id}")
        return channel_id
    else:
        print("Could not find channel ID")
        return None


# 运行函数
if __name__ == "__main__":
    get_channel_id()