# クレジットカード比較ナビ

クレジットカードの比較・アフィリエイトサイトの自動生成システムです。

## 概要

このプロジェクトは、クレジットカード情報をJSON形式で管理し、HTMLサイトを自動生成するシステムです。
ダイヤモンドZAiのクレジットカード比較サイトを参考に、オリジナルデザインで作成しています。

## 機能

- **カード情報管理**: JSON形式でクレジットカード情報を管理
- **HTML自動生成**: Pythonスクリプトでサイトを自動生成
- **レスポンシブデザイン**: PC・スマートフォン対応
- **カテゴリ分類**: 還元率、年会費、ゴールドカード等で分類
- **比較表機能**: 複数カードを一覧で比較
- **アフィリエイトリンク対応**: 各カードにアフィリエイトURLを設定可能

## ファイル構成

```
creditcard/
├── index.html          # メインページ（自動生成）
├── style.css           # スタイルシート
├── cards.json          # カード情報データ
└── README.md           # このファイル
```

## セットアップ

### 1. カード情報の編集

`cards.json` ファイルを編集してクレジットカード情報を追加・変更します。

```json
{
  "id": "card-001",
  "name": "カード名",
  "return_rate": "1.0〜5.0%",
  "annual_fee": "永年無料",
  "brand": ["VISA", "Mastercard"],
  "emoney": ["iD", "Apple Pay"],
  "features": [
    "特典1",
    "特典2",
    "特典3"
  ],
  "category": ["popular", "no-fee"],
  "gradient": "135deg, #667eea 0%, #764ba2 100%",
  "affiliate_url": "https://example.com/affiliate"
}
```

### 2. サイトの生成

```bash
cd /home/user/kyotei-ai-8
python tools/generate_creditcard.py
```

### 3. プレビュー

生成されたHTMLファイルをブラウザで開きます：

```bash
open creditcard/index.html
# または
firefox creditcard/index.html
```

## カスタマイズ

### カード情報の追加

`tools/generate_creditcard.py` の `CreditCardData` クラスの `get_default_cards()` メソッドを編集するか、
`cards.json` ファイルに直接追加します。

### デザインの変更

`creditcard/style.css` を編集してデザインをカスタマイズできます。

主なカラー変数：
- メインカラー（ピンク）: `#e91e63`
- アクセントカラー（ゴールド）: `#ffd700`
- 特別カラー（ブルー）: `#2196f3`

### アフィリエイトリンクの設定

各カードの `affiliate_url` フィールドに、実際のアフィリエイトリンクを設定します。

```json
{
  "affiliate_url": "https://your-affiliate-network.com/link?id=12345"
}
```

## デプロイ

### GitHub Pagesへのデプロイ

1. GitHubリポジトリの Settings → Pages
2. Source: `main` branch, `/creditcard` folder
3. Save

### 独自ドメインの設定

`creditcard/` ディレクトリに `CNAME` ファイルを追加：

```
your-domain.com
```

## 注意事項

### 法的事項

- アフィリエイト広告を利用する場合は、必ず「広告である旨」を明示してください
- 各クレジットカード会社の利用規約を確認してください
- 掲載する情報は定期的に更新し、最新の情報を提供してください

### プライバシー

- ユーザーの個人情報を取得する場合は、プライバシーポリシーを掲載してください
- Cookie等を利用する場合は、適切に通知してください

## トラブルシューティング

### スタイルが適用されない

`style.css` のパスが正しいか確認してください：

```html
<link rel="stylesheet" href="style.css">
```

### カード情報が表示されない

1. `cards.json` のJSON形式が正しいか確認
2. `generate_creditcard.py` を再実行
3. ブラウザのキャッシュをクリア

## ライセンス

このプロジェクトはオリジナルデザインで作成されています。
参考にしたサイト（ダイヤモンドZAi）のデザインを直接コピーしたものではありません。

## 更新履歴

- **2026-01-16**: 初版リリース
  - クレジットカード比較サイトの基本機能実装
  - 6種類のサンプルカード情報追加
  - レスポンシブデザイン対応
