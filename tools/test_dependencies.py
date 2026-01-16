#!/usr/bin/env python3
"""
依存関係のテストスクリプト
各ライブラリが正しくインストールされているか確認します
"""

print("=== 依存関係テスト ===\n")

# 1. gTTS
print("1. gTTS のテスト...")
try:
    from gtts import gTTS
    print("   ✓ gTTS インポート成功")
    # 簡単なテスト（ネットワーク不要のチェック）
    print("   ✓ gTTS 利用可能")
except Exception as e:
    print(f"   ✗ gTTS エラー: {e}")

# 2. Pillow
print("\n2. Pillow のテスト...")
try:
    from PIL import Image, ImageDraw, ImageFont
    print("   ✓ Pillow インポート成功")
    # 簡単な画像生成テスト
    img = Image.new('RGB', (100, 100), (255, 0, 0))
    print("   ✓ 画像生成成功")
except Exception as e:
    print(f"   ✗ Pillow エラー: {e}")

# 3. moviepy
print("\n3. moviepy のテスト...")
try:
    from moviepy.editor import ImageClip, AudioFileClip
    print("   ✓ moviepy インポート成功")
    print("   ✓ moviepy 利用可能")
except Exception as e:
    print(f"   ✗ moviepy エラー: {e}")

# 4. Google API Client
print("\n4. Google API Client のテスト...")
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    print("   ✓ Google API Client インポート成功")
    print("   ✓ Google API Client 利用可能")
except Exception as e:
    print(f"   ✗ Google API Client エラー: {e}")

print("\n=== テスト完了 ===")
