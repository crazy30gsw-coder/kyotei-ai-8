#!/usr/bin/env python3
"""
YouTube動画自動生成スクリプト

競艇予想の記事内容から音声と動画を生成し、YouTube にアップロードします。
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import json
import re

# 外部ライブラリのインポート（インストール後に有効化）
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("警告: gTTS がインストールされていません。音声生成には pip install gtts が必要です。")

# moviepyの代わりにffmpegコマンドを直接使用
import subprocess
FFMPEG_AVAILABLE = True
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    if result.returncode != 0:
        FFMPEG_AVAILABLE = False
        print("警告: ffmpeg がインストールされていません。動画生成には ffmpeg が必要です。")
except FileNotFoundError:
    FFMPEG_AVAILABLE = False
    print("警告: ffmpeg が見つかりません。動画生成には ffmpeg のインストールが必要です。")

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("警告: Pillow がインストールされていません。画像生成には pip install Pillow が必要です。")

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False
    print("警告: Google API Client がインストールされていません。YouTube アップロードには pip install google-auth-oauthlib google-api-python-client が必要です。")


# 設定
JST = timezone(timedelta(hours=9))
VIDEO_DIR = Path(__file__).parent.parent / "videos"
AUDIO_DIR = Path(__file__).parent.parent / "audio"
IMAGE_DIR = Path(__file__).parent.parent / "images"

# YouTube API設定
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = Path(__file__).parent.parent / "client_secrets.json"
TOKEN_FILE = Path(__file__).parent.parent / "token.json"


class VideoGenerator:
    """動画生成クラス"""

    def __init__(self):
        """初期化"""
        self.video_dir = VIDEO_DIR
        self.audio_dir = AUDIO_DIR
        self.image_dir = IMAGE_DIR

        # ディレクトリ作成
        self.video_dir.mkdir(exist_ok=True)
        self.audio_dir.mkdir(exist_ok=True)
        self.image_dir.mkdir(exist_ok=True)

    def extract_text_from_html(self, html_path: Path) -> dict:
        """
        HTMLファイルからテキストを抽出

        Args:
            html_path: HTMLファイルのパス

        Returns:
            抽出されたテキスト情報の辞書
        """
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # タイトルを抽出
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content)
        title = title_match.group(1) if title_match else "競艇予想"

        # 本文を抽出（HTMLタグを除去）
        content = re.sub(r'<[^>]+>', '', html_content)
        content = re.sub(r'\s+', ' ', content).strip()

        # 日付を抽出
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', html_path.name)
        date_str = date_match.group(1) if date_match else datetime.now(JST).strftime('%Y-%m-%d')

        return {
            'title': title,
            'content': content,
            'date': date_str
        }

    def generate_audio(self, text: str, output_path: Path, lang: str = 'ja') -> bool:
        """
        テキストから音声ファイルを生成

        Args:
            text: 音声にするテキスト
            output_path: 出力ファイルパス
            lang: 言語コード（デフォルト: 'ja'）

        Returns:
            成功したかどうか
        """
        if not GTTS_AVAILABLE:
            print("エラー: gTTS が利用できません")
            return False

        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(str(output_path))
            print(f"音声ファイルを生成しました: {output_path}")
            return True
        except Exception as e:
            print(f"音声生成エラー: {e}")
            return False

    def create_thumbnail(self, title: str, date: str, output_path: Path) -> bool:
        """
        サムネイル画像を生成

        Args:
            title: タイトル
            date: 日付
            output_path: 出力ファイルパス

        Returns:
            成功したかどうか
        """
        if not PIL_AVAILABLE:
            print("エラー: Pillow が利用できません")
            return False

        try:
            # 画像サイズ（YouTube推奨: 1280x720）
            width, height = 1280, 720

            # 背景色（青系）
            bg_color = (0, 102, 204)

            # 画像作成
            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)

            # テキスト描画
            # タイトル
            title_text = "競艇予想"
            try:
                # システムフォントを試す
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
                font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
            except:
                # フォントが見つからない場合はデフォルトフォント
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()

            # タイトルを中央に配置
            title_bbox = draw.textbbox((0, 0), title_text, font=font_large)
            title_w = title_bbox[2] - title_bbox[0]
            title_x = (width - title_w) // 2
            draw.text((title_x, 200), title_text, fill=(255, 255, 255), font=font_large)

            # 日付を配置
            date_bbox = draw.textbbox((0, 0), date, font=font_medium)
            date_w = date_bbox[2] - date_bbox[0]
            date_x = (width - date_w) // 2
            draw.text((date_x, 400), date, fill=(255, 255, 255), font=font_medium)

            # 保存
            img.save(output_path)
            print(f"サムネイル画像を生成しました: {output_path}")
            return True
        except Exception as e:
            print(f"画像生成エラー: {e}")
            return False

    def create_video(self, image_path: Path, audio_path: Path, output_path: Path) -> bool:
        """
        画像と音声から動画を生成（ffmpegを使用）

        Args:
            image_path: 画像ファイルパス
            audio_path: 音声ファイルパス
            output_path: 出力動画ファイルパス

        Returns:
            成功したかどうか
        """
        if not FFMPEG_AVAILABLE:
            print("エラー: ffmpeg が利用できません")
            return False

        try:
            # ffmpegコマンドで画像と音声を結合
            # -loop 1: 画像をループ
            # -i image: 入力画像
            # -i audio: 入力音声
            # -c:v libx264: H.264ビデオコーデック
            # -c:a aac: AACオーディオコーデック
            # -shortest: 音声の長さに合わせる
            # -pix_fmt yuv420p: 互換性のあるピクセルフォーマット
            # -r 24: フレームレート24fps
            cmd = [
                'ffmpeg',
                '-y',  # 既存ファイルを上書き
                '-loop', '1',
                '-i', str(image_path),
                '-i', str(audio_path),
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                '-pix_fmt', 'yuv420p',
                '-r', '24',
                str(output_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"動画ファイルを生成しました: {output_path}")
                return True
            else:
                print(f"動画生成エラー: {result.stderr}")
                return False

        except Exception as e:
            print(f"動画生成エラー: {e}")
            return False


class YouTubeUploader:
    """YouTube アップローダークラス"""

    def __init__(self):
        """初期化"""
        self.credentials = None
        self.youtube = None

    def authenticate(self) -> bool:
        """
        YouTube API の認証

        Returns:
            認証が成功したかどうか
        """
        if not YOUTUBE_API_AVAILABLE:
            print("エラー: Google API Client が利用できません")
            return False

        try:
            # トークンファイルがあれば読み込み
            if TOKEN_FILE.exists():
                self.credentials = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

            # 認証情報がないか、無効な場合は再認証
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    if not CLIENT_SECRETS_FILE.exists():
                        print(f"エラー: クライアントシークレットファイルが見つかりません: {CLIENT_SECRETS_FILE}")
                        return False

                    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
                    self.credentials = flow.run_local_server(port=0)

                # トークンを保存
                with open(TOKEN_FILE, 'w') as token:
                    token.write(self.credentials.to_json())

            # YouTube API クライアントを構築
            self.youtube = build('youtube', 'v3', credentials=self.credentials)
            print("YouTube API 認証成功")
            return True
        except Exception as e:
            print(f"認証エラー: {e}")
            return False

    def upload_video(self, video_path: Path, title: str, description: str,
                    category_id: str = "22", privacy_status: str = "private") -> Optional[str]:
        """
        YouTube に動画をアップロード

        Args:
            video_path: 動画ファイルパス
            title: 動画タイトル
            description: 動画の説明
            category_id: カテゴリID（デフォルト: "22" = People & Blogs）
            privacy_status: 公開設定（public, private, unlisted）

        Returns:
            アップロードされた動画のURL（失敗時はNone）
        """
        if not self.youtube:
            print("エラー: YouTube API が初期化されていません")
            return None

        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': privacy_status
                }
            }

            media = MediaFileUpload(str(video_path), resumable=True)

            request = self.youtube.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"アップロード進行状況: {int(status.progress() * 100)}%")

            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"アップロード成功: {video_url}")
            return video_url
        except Exception as e:
            print(f"アップロードエラー: {e}")
            return None


def main():
    """メイン処理"""
    print("=== YouTube 動画自動生成スクリプト ===\n")

    # 今日の日付
    today = datetime.now(JST).strftime('%Y-%m-%d')

    # HTMLファイルのパス
    html_path = Path(__file__).parent.parent / "posts" / f"{today}.html"

    if not html_path.exists():
        print(f"エラー: HTMLファイルが見つかりません: {html_path}")
        print("まず generate.py を実行してHTMLファイルを生成してください。")
        sys.exit(1)

    # 動画生成
    generator = VideoGenerator()

    print("1. HTMLからテキストを抽出...")
    text_data = generator.extract_text_from_html(html_path)
    print(f"   タイトル: {text_data['title']}")
    print(f"   日付: {text_data['date']}")

    # ファイルパス設定
    audio_path = generator.audio_dir / f"{today}.mp3"
    image_path = generator.image_dir / f"{today}.png"
    video_path = generator.video_dir / f"{today}.mp4"

    # 音声生成用のテキストを作成
    script_text = f"{text_data['title']}。{text_data['content'][:200]}"  # 最初の200文字

    print("\n2. 音声ファイルを生成...")
    if not generator.generate_audio(script_text, audio_path):
        print("音声生成に失敗しました")
        sys.exit(1)

    print("\n3. サムネイル画像を生成...")
    if not generator.create_thumbnail(text_data['title'], text_data['date'], image_path):
        print("画像生成に失敗しました")
        sys.exit(1)

    print("\n4. 動画を生成...")
    if not generator.create_video(image_path, audio_path, video_path):
        print("動画生成に失敗しました")
        sys.exit(1)

    print("\n5. YouTube へのアップロード...")
    uploader = YouTubeUploader()

    if uploader.authenticate():
        video_url = uploader.upload_video(
            video_path,
            title=f"{text_data['title']} - {text_data['date']}",
            description=f"競艇予想の自動生成動画です。\n日付: {text_data['date']}",
            privacy_status="private"  # デフォルトは非公開
        )

        if video_url:
            print(f"\n✅ 完了！動画URL: {video_url}")
        else:
            print("\n⚠️ 動画は生成されましたが、アップロードに失敗しました")
            print(f"   ローカルの動画: {video_path}")
    else:
        print("\n⚠️ YouTube認証に失敗しました。動画はローカルに保存されています")
        print(f"   ローカルの動画: {video_path}")

    print("\n=== 処理完了 ===")


if __name__ == "__main__":
    main()
