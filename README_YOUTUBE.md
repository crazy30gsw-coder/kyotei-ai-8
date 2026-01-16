# YouTube動画自動生成ガイド

## 概要

このツールは、競艇予想のHTML記事から自動的にYouTube動画を生成してアップロードします。

## 機能

1. **テキスト抽出**: HTML記事からタイトルと本文を抽出
2. **音声生成**: Google Text-to-Speech（gTTS）を使用してテキストを音声に変換
3. **サムネイル生成**: Pillowを使用してサムネイル画像を作成
4. **動画生成**: moviepyを使用して画像と音声を組み合わせて動画を作成
5. **YouTubeアップロード**: YouTube Data API v3を使用して動画をアップロード

## セットアップ

### 1. 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成し、APIキーを設定します。

```bash
cp .env.example .env
```

`.env` ファイルを編集して、OpenAI APIキーを設定してください：

```bash
# OpenAI APIキー（必要な場合）
OPENAI_API_KEY=sk-...your_actual_api_key_here...
# または
KKK=sk-...your_actual_api_key_here...
```

**OpenAI APIキーの取得方法：**
1. [OpenAI Platform](https://platform.openai.com/api-keys) にアクセス
2. サインイン/サインアップ
3. 「Create new secret key」をクリック
4. 生成されたキーをコピーして `.env` ファイルに貼り付け

**注意**: `.env` ファイルは `.gitignore` で除外されているため、Gitリポジトリにはコミットされません。

### 2. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 3. YouTube API の設定

#### 3.1 Google Cloud Console で設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成（または既存のプロジェクトを選択）
3. **YouTube Data API v3** を有効にする
   - 左メニューから「APIとサービス」→「ライブラリ」
   - 「YouTube Data API v3」を検索して有効化
4. **OAuth 2.0 クライアント ID** を作成
   - 「APIとサービス」→「認証情報」
   - 「認証情報を作成」→「OAuth クライアント ID」
   - アプリケーションの種類: 「デスクトップ アプリ」
   - 名前: 任意（例: YouTube Video Generator）
5. **クライアントシークレットをダウンロード**
   - 作成したクライアント IDの右側の「↓」アイコンをクリック
   - JSONファイルをダウンロード

#### 3.2 クライアントシークレットの配置

ダウンロードしたJSONファイルを `client_secrets.json` という名前でプロジェクトルートに配置します。

```bash
mv ~/Downloads/client_secret_XXXXX.json /home/user/kyotei-ai-8/client_secrets.json
```

### 4. システムフォントのインストール（オプション）

サムネイル画像の日本語表示のために、日本語フォントをインストールすることをおすすめします。

```bash
# Debian/Ubuntu
sudo apt-get install fonts-noto-cjk

# macOS（Homebrew）
brew tap homebrew/cask-fonts
brew install --cask font-noto-sans-cjk-jp
```

## 使い方

### 基本的な使い方

1. **HTML記事を生成**（既存のツール）

```bash
python tools/generate.py
```

2. **YouTube動画を生成してアップロード**

```bash
python tools/youtube_video_generator.py
```

### 初回実行時の認証

初回実行時にブラウザが開き、Googleアカウントでの認証が求められます。

1. ブラウザが自動的に開きます
2. Googleアカウントでログイン
3. アプリケーションにYouTubeへのアクセスを許可
4. 認証が完了すると `token.json` が自動的に作成されます

次回以降は認証をスキップできます。

### 出力ファイル

- **音声**: `audio/YYYY-MM-DD.mp3`
- **画像**: `images/YYYY-MM-DD.png`
- **動画**: `videos/YYYY-MM-DD.mp4`

## カスタマイズ

### 音声の変更

`youtube_video_generator.py` の以下の行を編集：

```python
# 音声の言語を変更
generator.generate_audio(script_text, audio_path, lang='en')  # 英語の場合

# 音声の速度を変更
tts = gTTS(text=text, lang=lang, slow=True)  # ゆっくり話す
```

### サムネイルのデザイン変更

`create_thumbnail()` メソッド内の以下のパラメータを編集：

```python
# 背景色
bg_color = (0, 102, 204)  # RGB値

# フォントサイズ
font_large = ImageFont.truetype("...", 80)  # タイトル
font_medium = ImageFont.truetype("...", 50)  # 日付
```

### アップロード設定の変更

`main()` 関数内の `upload_video()` 呼び出しを編集：

```python
video_url = uploader.upload_video(
    video_path,
    title=f"カスタムタイトル - {text_data['date']}",
    description="カスタム説明文",
    privacy_status="public"  # public, private, unlisted
)
```

## トラブルシューティング

### エラー: gTTS が利用できません

```bash
pip install gtts
```

### エラー: moviepy が利用できません

```bash
pip install moviepy
```

moviepyはffmpegに依存しています。システムにffmpegがインストールされていることを確認してください：

```bash
# Debian/Ubuntu
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### エラー: Google API Client が利用できません

```bash
pip install google-auth-oauthlib google-api-python-client
```

### エラー: クライアントシークレットファイルが見つかりません

`client_secrets.json` がプロジェクトルートに配置されていることを確認してください。

### YouTubeアップロードのクォータ制限

YouTube Data API v3には1日あたりのクォータ制限があります（デフォルト: 10,000ユニット）。
動画のアップロードは1回あたり約1,600ユニットを消費します。

クォータを確認：
- [Google Cloud Console](https://console.cloud.google.com/) → 「APIとサービス」→「ダッシュボード」

## 自動化（GitHub Actions）

GitHub Actionsで自動実行する場合は、以下の設定が必要です：

1. **シークレットの設定**
   - リポジトリの Settings → Secrets and variables → Actions
   - `YOUTUBE_CLIENT_SECRETS`: client_secrets.jsonの内容
   - `YOUTUBE_TOKEN`: token.jsonの内容（初回認証後）

2. **ワークフローファイルの編集**
   `.github/workflows/daily.yml` に動画生成ステップを追加

## ライセンス

このツールは既存のkyotei-aiプロジェクトの一部です。

## サポート

問題が発生した場合は、GitHubのIssuesで報告してください。
