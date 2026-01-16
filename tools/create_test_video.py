#!/usr/bin/env python3
"""
テスト用の簡易動画生成スクリプト
gTTSの代わりに、無音の音声ファイルを生成してテストします
"""

import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ディレクトリ作成
video_dir = Path(__file__).parent.parent / "videos"
audio_dir = Path(__file__).parent.parent / "audio"
image_dir = Path(__file__).parent.parent / "images"

video_dir.mkdir(exist_ok=True)
audio_dir.mkdir(exist_ok=True)
image_dir.mkdir(exist_ok=True)

print("=== テスト用動画生成 ===\n")

# 1. サムネイル画像を生成
print("1. サムネイル画像を生成...")
image_path = image_dir / "test.png"

width, height = 1280, 720
bg_color = (0, 102, 204)

img = Image.new('RGB', (width, height), bg_color)
draw = ImageDraw.Draw(img)

title_text = "競艇予想 テスト動画"
date_text = "2026-01-16"

try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()

# タイトルを中央に配置
title_bbox = draw.textbbox((0, 0), title_text, font=font_large)
title_w = title_bbox[2] - title_bbox[0]
title_x = (width - title_w) // 2
draw.text((title_x, 200), title_text, fill=(255, 255, 255), font=font_large)

# 日付を配置
date_bbox = draw.textbbox((0, 0), date_text, font=font_medium)
date_w = date_bbox[2] - date_bbox[0]
date_x = (width - date_w) // 2
draw.text((date_x, 400), date_text, fill=(255, 255, 255), font=font_medium)

img.save(image_path)
print(f"   ✓ サムネイル生成完了: {image_path}")

# 2. テスト用の無音音声を生成（5秒間）
print("\n2. テスト用音声を生成（5秒間の無音）...")
audio_path = audio_dir / "test.mp3"

# ffmpegで5秒間の無音音声を生成
cmd = [
    'ffmpeg',
    '-y',
    '-f', 'lavfi',
    '-i', 'anullsrc=r=44100:cl=stereo',
    '-t', '5',
    '-q:a', '9',
    '-acodec', 'libmp3lame',
    str(audio_path)
]

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"   ✓ 音声生成完了: {audio_path}")
else:
    print(f"   ✗ 音声生成エラー: {result.stderr}")
    exit(1)

# 3. 動画を生成
print("\n3. 動画を生成...")
video_path = video_dir / "test.mp4"

cmd = [
    'ffmpeg',
    '-y',
    '-loop', '1',
    '-i', str(image_path),
    '-i', str(audio_path),
    '-c:v', 'libx264',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    '-pix_fmt', 'yuv420p',
    '-r', '24',
    str(video_path)
]

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"   ✓ 動画生成完了: {video_path}")
    print(f"\n=== 成功！ ===")
    print(f"動画ファイル: {video_path}")
    print(f"動画サイズ: {video_path.stat().st_size / 1024:.2f} KB")
else:
    print(f"   ✗ 動画生成エラー: {result.stderr}")
    exit(1)
