import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Driveのアップロード権限（ファイルのアップロード＆共有）
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_pdf(file_path):
    # フルパスのファイル存在を確実に確認
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"ファイルが見つかりません：{file_path}")

    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # 誰でも閲覧可能にする権限設定
    service.permissions().create(
        fileId=uploaded_file['id'],
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()

    file_url = f"https://drive.google.com/file/d/{uploaded_file['id']}/view?usp=sharing"
    return file_url

if __name__ == "__main__":
    print("アップロードしたいPDFファイルの絶対パスを入力してください。")
    print("例: /Users/tsukarintaro/Desktop/feedback/suzuki100m.pdf")
    file_path = input("> ").strip()

    try:
        link = upload_pdf(file_path)
        print("✅ アップロード成功！共有リンクはこちら:")
        print(link)
    except FileNotFoundError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

