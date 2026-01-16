#!/usr/bin/env python3
"""
クレジットカード比較サイト自動生成スクリプト

カード情報を管理し、HTMLページを自動生成します。
"""

from datetime import datetime, timezone, timedelta
from pathlib import Path
import json
from typing import List, Dict

# 設定
JST = timezone(timedelta(hours=9))
BASE_DIR = Path(__file__).parent.parent
CREDIT_DIR = BASE_DIR / "creditcard"
CARDS_JSON = CREDIT_DIR / "cards.json"


class CreditCardData:
    """クレジットカードデータ管理クラス"""

    def __init__(self):
        self.cards = []
        self.load_cards()

    def load_cards(self):
        """カード情報をJSONから読み込み"""
        if CARDS_JSON.exists():
            with open(CARDS_JSON, 'r', encoding='utf-8') as f:
                self.cards = json.load(f)
        else:
            # デフォルトのカード情報
            self.cards = self.get_default_cards()
            self.save_cards()

    def save_cards(self):
        """カード情報をJSONに保存"""
        CREDIT_DIR.mkdir(exist_ok=True)
        with open(CARDS_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.cards, f, ensure_ascii=False, indent=2)

    def get_default_cards(self) -> List[Dict]:
        """デフォルトのカード情報"""
        return [
            {
                "id": "premium-001",
                "name": "高還元率プレミアムカード",
                "return_rate": "1.0〜5.0%",
                "annual_fee": "永年無料",
                "brand": ["VISA", "Mastercard"],
                "emoney": ["iD", "Apple Pay"],
                "features": [
                    "年会費永年無料",
                    "ポイント還元率最大5.0%",
                    "新規入会で最大5,000ポイント",
                    "家族カード無料"
                ],
                "category": ["popular", "no-fee", "return-rate"],
                "gradient": "135deg, #667eea 0%, #764ba2 100%",
                "affiliate_url": "#"
            },
            {
                "id": "rakuten-001",
                "name": "楽天スタイルカード",
                "return_rate": "1.0〜3.0%",
                "annual_fee": "永年無料",
                "brand": ["VISA", "JCB"],
                "emoney": ["楽天Edy", "Apple Pay"],
                "features": [
                    "楽天市場でポイント3倍",
                    "楽天ポイントがザクザク貯まる",
                    "年会費永年無料",
                    "楽天サービスでお得"
                ],
                "category": ["popular", "no-fee", "mile"],
                "gradient": "135deg, #f093fb 0%, #f5576c 100%",
                "affiliate_url": "#"
            },
            {
                "id": "gold-001",
                "name": "ゴールドカードプレミアム",
                "return_rate": "0.5〜10.0%",
                "annual_fee": "1,375円",
                "brand": ["VISA", "Mastercard", "JCB"],
                "emoney": ["iD", "QUICPay", "Apple Pay"],
                "features": [
                    "空港ラウンジ無料",
                    "最大1億円の海外旅行保険",
                    "ポイント還元率最大10.0%",
                    "ゴールド限定特典"
                ],
                "category": ["popular", "gold", "insurance"],
                "gradient": "135deg, #ffd89b 0%, #19547b 100%",
                "affiliate_url": "#"
            },
            {
                "id": "platinum-001",
                "name": "プラチナカードエクセレント",
                "return_rate": "1.0〜5.0%",
                "annual_fee": "22,000円",
                "brand": ["VISA", "Mastercard"],
                "emoney": ["iD", "Apple Pay", "QUICPay"],
                "features": [
                    "24時間コンシェルジュサービス",
                    "プライオリティ・パス無料",
                    "最高1億円の旅行保険",
                    "レストラン優待"
                ],
                "category": ["platinum", "insurance"],
                "gradient": "135deg, #434343 0%, #000000 100%",
                "affiliate_url": "#"
            },
            {
                "id": "student-001",
                "name": "学生専用カード",
                "return_rate": "0.5〜2.0%",
                "annual_fee": "在学中無料",
                "brand": ["VISA"],
                "emoney": ["iD", "Apple Pay"],
                "features": [
                    "学生限定の特典",
                    "卒業後も年会費優遇",
                    "海外旅行保険付帯",
                    "ポイント交換先豊富"
                ],
                "category": ["no-fee", "instant"],
                "gradient": "135deg, #4facfe 0%, #00f2fe 100%",
                "affiliate_url": "#"
            },
            {
                "id": "business-001",
                "name": "ビジネスカードプロ",
                "return_rate": "0.5〜1.5%",
                "annual_fee": "初年度無料（2年目以降1,375円）",
                "brand": ["VISA", "Mastercard", "JCB"],
                "emoney": ["iD", "QUICPay"],
                "features": [
                    "経費管理が簡単",
                    "ビジネス特典充実",
                    "ETCカード複数枚発行可能",
                    "会計ソフト連携"
                ],
                "category": ["business", "etc"],
                "gradient": "135deg, #89f7fe 0%, #66a6ff 100%",
                "affiliate_url": "#"
            }
        ]

    def add_card(self, card_data: Dict):
        """カードを追加"""
        self.cards.append(card_data)
        self.save_cards()

    def get_cards_by_category(self, category: str) -> List[Dict]:
        """カテゴリでフィルタリング"""
        return [card for card in self.cards if category in card.get("category", [])]


class HTMLGenerator:
    """HTML生成クラス"""

    def __init__(self, card_data: CreditCardData):
        self.card_data = card_data

    def generate_card_html(self, card: Dict) -> str:
        """カードHTML生成"""
        features_html = "\n".join([
            f'                        <li>\n'
            f'                            <span class="feature-label">{feat.split("：")[0] if "：" in feat else "特典"}</span>\n'
            f'                            <span class="feature-value">{feat.split("：")[1] if "：" in feat else feat}</span>\n'
            f'                        </li>'
            for feat in card.get("features", [])[:4]
        ])

        brands = " / ".join(card.get("brand", []))
        card_id = card.get("id", "")

        return f'''                <div class="card-item">
                    <img src="images/{card_id}.png" alt="{card["name"]}" style="width: 100%; height: auto; border-radius: 10px; margin-bottom: 15px;">
                    <h3 class="card-item-title">{card["name"]}</h3>
                    <ul class="card-features">
                        <li>
                            <span class="feature-label">還元率</span>
                            <span class="feature-value">{card["return_rate"]}</span>
                        </li>
                        <li>
                            <span class="feature-label">年会費</span>
                            <span class="feature-value">{card["annual_fee"]}</span>
                        </li>
                        <li>
                            <span class="feature-label">ブランド</span>
                            <span class="feature-value">{brands}</span>
                        </li>
{features_html}
                    </ul>
                    <a href="{card.get("affiliate_url", "#")}" class="apply-btn" style="width: 100%; text-align: center;" target="_blank" rel="noopener">詳細を見る</a>
                </div>'''

    def generate_comparison_table_row(self, card: Dict) -> str:
        """比較表の行を生成"""
        brands = "<br>".join(card.get("brand", []))
        emoney = "<br>".join(card.get("emoney", []))
        card_id = card.get("id", "")

        return f'''                        <tr>
                            <td><strong style="font-size: 18px; color: #e91e63;">{card["return_rate"]}</strong></td>
                            <td><strong style="color: {"#4caf50" if "無料" in card["annual_fee"] else "#333"};">{card["annual_fee"]}</strong></td>
                            <td>{brands}</td>
                            <td>{emoney}</td>
                            <td><img src="images/{card_id}.png" alt="{card["name"]}" class="card-image"></td>
                            <td><a href="{card.get("affiliate_url", "#")}" class="apply-btn" target="_blank" rel="noopener">詳細・申込</a></td>
                        </tr>'''

    def generate_index_html(self):
        """index.htmlを生成"""
        today = datetime.now(JST).strftime('%Y年%m月%d日')

        # 人気カード（最初の3枚）
        popular_cards = self.card_data.cards[:3]
        popular_cards_html = "\n".join([self.generate_card_html(card) for card in popular_cards])

        # 比較表（全カード）
        comparison_rows = "\n".join([self.generate_comparison_table_row(card) for card in self.card_data.cards])

        # 年会費無料カード
        no_fee_cards = self.card_data.get_cards_by_category("no-fee")
        no_fee_cards_html = "\n".join([self.generate_card_html(card) for card in no_fee_cards[:3]])

        html_template = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>クレジットカード比較ナビ | お得なカード選びをサポート</title>
    <meta name="description" content="2026年最新！おすすめクレジットカードを徹底比較。年会費無料、高還元率、ゴールドカードなどカテゴリ別に紹介します。">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- ヘッダー -->
    <header class="header">
        <div class="header-container">
            <a href="/" class="site-title">💳 クレジットカード比較ナビ</a>
            <nav>
                <ul class="nav-menu">
                    <li><a href="#recommend">おすすめ</a></li>
                    <li><a href="#compare">比較表</a></li>
                    <li><a href="#category">カテゴリ</a></li>
                    <li><a href="#guide">選び方</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- お知らせバー -->
    <div class="container">
        <div class="notice-bar">
            ⚠️ 当サイトではアフィリエイト広告を利用しています
        </div>
    </div>

    <!-- メインコンテンツ -->
    <main class="container">
        <!-- カテゴリボタン -->
        <section id="category">
            <div class="update-date">{today}更新</div>
            <h2 class="section-title">カテゴリから選ぶ</h2>
            <div class="category-buttons">
                <a href="#return-rate" class="category-btn">還元率で選ぶ</a>
                <a href="#popular" class="category-btn featured">🔥 人気カードで選ぶ</a>
                <a href="#gold" class="category-btn">ゴールドカードで選ぶ</a>
                <a href="#platinum" class="category-btn">プラチナカードで選ぶ</a>
                <a href="#etc" class="category-btn">ETCカードで選ぶ</a>
                <a href="#amex" class="category-btn special">アメックスで選ぶ</a>
                <a href="#mile" class="category-btn">マイルで選ぶ</a>
                <a href="#no-fee" class="category-btn">年会費無料で選ぶ</a>
                <a href="#insurance" class="category-btn">海外旅行保険で選ぶ</a>
                <a href="#instant" class="category-btn">即日発行で選ぶ</a>
                <a href="#business" class="category-btn">法人カードで選ぶ</a>
                <a href="#best" class="category-btn featured">⭐ 最強カードで選ぶ</a>
            </div>
        </section>

        <!-- おすすめクレジットカード -->
        <section id="recommend" class="section">
            <h2 class="section-title">おすすめクレジットカードはこれだ！</h2>
            <p style="margin-bottom: 20px;">
                {today}最新情報！クレジットカードの還元率や年会費、付帯特典のサービス内容などを比較して「おすすめクレジットカード」を厳選しました。
                年会費無料で高還元なカード、お得なゴールドカード、マイルが貯まりやすいカードなど、目的別に最適なカードをご紹介します。
            </p>

            <h3 style="font-size: 20px; margin: 30px 0 15px 0; color: #333;">還元率、年会費などで比較！人気のおすすめクレジットカード</h3>

            <div class="card-comparison">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>還元率</th>
                            <th>年会費<br>(税込)</th>
                            <th>ブランド</th>
                            <th>電子マネー<br>対応</th>
                            <th>カード<br>フェイス</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
{comparison_rows}
                    </tbody>
                </table>
            </div>
        </section>

        <!-- カードグリッド -->
        <section id="popular" class="section">
            <h2 class="section-title">人気クレジットカード</h2>
            <div class="card-grid">
{popular_cards_html}
            </div>
        </section>

        <!-- ジャンル別リンク -->
        <section class="section link-section">
            <h2 class="section-title">ジャンル別の「おすすめクレジットカード」</h2>
            <p style="margin-bottom: 20px;">
                還元率クレジットカードや、日常が豊かになる豪華特典を使えるプラチナカードなど、
                ジャンルごとにさまざまなカードを徹底比較したので、ぜひ、自分にピッタリなクレジットカードを見つけるための参考にして欲しい。
            </p>
            <ul class="link-list">
                <li><a href="#no-fee">年会費無料の高還元クレジットカード</a></li>
                <li><a href="#platinum">付帯特典充実おすすめプラチナカード</a></li>
                <li><a href="#cospa">コスパに優れたお得なゴールドカード</a></li>
                <li><a href="#mile">マイルが貯まりやすいクレジットカード</a></li>
                <li><a href="#etc-free">ETCカードが無料のクレジットカード</a></li>
                <li><a href="#business">業務効率もアップするお得な法人カード</a></li>
            </ul>
        </section>

        <!-- 年会費無料セクション -->
        <section id="no-fee" class="section">
            <h2 class="section-title">おすすめの「年会費無料の高還元クレジットカード」！</h2>
            <p style="margin-bottom: 20px;">
                クレジットカードを初めて作る人や、節約効果の高いカードが欲しい人などにおすすめなのが「年会費無料の高還元クレジットカード」だ。
                年会費というコストをかけずに、日々の買い物でお得にポイントを獲得できるほか、使い方次第で年間数万円分のポイントが貯まることも！
            </p>
            <div class="card-grid">
{no_fee_cards_html}
            </div>
        </section>
    </main>

    <!-- フッター -->
    <footer class="footer">
        <div class="footer-links">
            <a href="#about">サイトについて</a>
            <a href="#privacy">プライバシーポリシー</a>
            <a href="#contact">お問い合わせ</a>
            <a href="#sitemap">サイトマップ</a>
        </div>
        <p>&copy; 2026 クレジットカード比較ナビ All Rights Reserved.</p>
        <div class="disclaimer">
            ※ 本サイトの情報は、各クレジットカード会社の公式サイトを基に作成しています。<br>
            ※ 掲載内容は予告なく変更される場合があります。最新情報は各社公式サイトでご確認ください。<br>
            ※ 当サイトではアフィリエイトプログラムを利用して商品を紹介しています。
        </div>
    </footer>
</body>
</html>'''

        # HTMLを保存
        CREDIT_DIR.mkdir(exist_ok=True)
        output_path = CREDIT_DIR / "index.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)

        print(f"✅ HTMLを生成しました: {output_path}")


def main():
    """メイン処理"""
    print("=== クレジットカード比較サイト生成 ===\n")

    # カードデータ読み込み
    card_data = CreditCardData()
    print(f"📊 {len(card_data.cards)}枚のカード情報を読み込みました")

    # HTML生成
    generator = HTMLGenerator(card_data)
    generator.generate_index_html()

    print("\n✅ 生成完了！")
    print(f"サイトURL: file://{CREDIT_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
