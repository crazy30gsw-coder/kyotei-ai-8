#!/usr/bin/env python3
"""
クレジットカード画像生成スクリプト

グラデーション背景のカード画像を生成します。
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json

# 設定
BASE_DIR = Path(__file__).parent.parent
CREDIT_DIR = BASE_DIR / "creditcard"
IMAGES_DIR = CREDIT_DIR / "images"
CARDS_JSON = CREDIT_DIR / "cards.json"


def create_card_image(card_data: dict, output_path: Path):
    """クレジットカード画像を生成"""
    # カードサイズ（横長）
    width, height = 400, 252  # クレジットカードの標準的なアスペクト比

    # グラデーションをパース
    gradient = card_data.get("gradient", "135deg, #667eea 0%, #764ba2 100%")
    # 簡易的にグラデーションの色を抽出
    colors = []
    parts = gradient.split(",")
    for part in parts:
        if "#" in part:
            color = part.split("#")[1].strip()
            if "%" in color:
                color = color.split("%")[0].strip()
            # 6桁のHEXコードを取得
            if len(color) >= 6:
                color = color[:6]
                try:
                    rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
                    colors.append(rgb)
                except:
                    pass

    if len(colors) < 2:
        colors = [(102, 126, 234), (118, 75, 162)]  # デフォルト

    # 画像作成
    img = Image.new('RGB', (width, height), colors[0])
    draw = ImageDraw.Draw(img)

    # グラデーション効果
    for y in range(height):
        ratio = y / height
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # カード名を描画
    try:
        # フォントを試す
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # カード名（最大15文字）
    card_name = card_data["name"][:15]

    # テキストを中央に配置
    text_bbox = draw.textbbox((0, 0), card_name, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    text_x = (width - text_w) // 2
    text_y = (height - text_h) // 2 - 20

    # 影を描画
    draw.text((text_x + 2, text_y + 2), card_name, fill=(0, 0, 0, 128), font=font)
    # テキストを描画
    draw.text((text_x, text_y), card_name, fill=(255, 255, 255), font=font)

    # 還元率を描画
    return_rate = card_data["return_rate"]
    rate_text = f"還元率 {return_rate}"
    rate_bbox = draw.textbbox((0, 0), rate_text, font=font_small)
    rate_w = rate_bbox[2] - rate_bbox[0]
    rate_x = (width - rate_w) // 2
    rate_y = text_y + text_h + 20
    draw.text((rate_x + 1, rate_y + 1), rate_text, fill=(0, 0, 0, 128), font=font_small)
    draw.text((rate_x, rate_y), rate_text, fill=(255, 255, 255), font=font_small)

    # 年会費を描画
    fee_text = card_data["annual_fee"]
    fee_bbox = draw.textbbox((0, 0), fee_text, font=font_small)
    fee_w = fee_bbox[2] - fee_bbox[0]
    fee_x = (width - fee_w) // 2
    fee_y = rate_y + 30
    draw.text((fee_x + 1, fee_y + 1), fee_text, fill=(0, 0, 0, 128), font=font_small)
    draw.text((fee_x, fee_y), fee_text, fill=(255, 255, 255), font=font_small)

    # 角を丸くする
    img = img.convert("RGBA")
    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, width, height], radius=20, fill=255)

    # マスクを適用
    output = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)

    # 保存
    output.save(output_path, 'PNG')
    print(f"✓ 生成: {output_path.name}")


def main():
    """メイン処理"""
    print("=== クレジットカード画像生成 ===\n")

    # 出力ディレクトリ作成
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # カードデータを読み込み
    with open(CARDS_JSON, 'r', encoding='utf-8') as f:
        cards = json.load(f)

    print(f"📊 {len(cards)}枚のカード画像を生成します\n")

    # 各カードの画像を生成
    for card in cards:
        card_id = card["id"]
        output_path = IMAGES_DIR / f"{card_id}.png"
        create_card_image(card, output_path)

    print(f"\n✅ 完了！{len(cards)}枚の画像を生成しました")
    print(f"出力先: {IMAGES_DIR}")


if __name__ == "__main__":
    main()
