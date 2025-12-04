# Gemini API利用ガイド

このドキュメントでは、プロジェクトでGoogle AI StudioのGemini APIやGCPのVertex AIを利用する方法を説明します。

## Google AI / GCPサービス設定

プロジェクトでGoogle AI StudioのGemini APIやGCPのサービスを利用できます。

### GOOGLE_API_KEY（Google AI Studio）

**用途**: Google AI StudioのGemini APIを使用する場合に設定します。

**取得方法**:
1. [Google AI Studio](https://aistudio.google.com/)にアクセス
2. 「Get API key」をクリック
3. APIキーを発行（既存のGoogle Cloudプロジェクトまたは新規プロジェクトを選択）
4. 発行されたAPIキーをコピー

**設定方法**:

`.env`ファイルに以下を追加：

```env
GOOGLE_API_KEY=your-api-key-here
```

**Pythonコードでの使用例**:

```python
import os
import google.generativeai as genai

# APIキーを設定
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# モデルを使用
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("こんにちは")
print(response.text)
```

**必要なPythonパッケージ**:

```bash
pip install google-generativeai
```

または`requirements.txt`に追加：

```
google-generativeai
```

### GOOGLE_APPLICATION_CREDENTIALS（GCP Vertex AI）

**用途**: GCPのVertex AI（Gemini API）や他のGCPサービスを使用する場合に設定します。

**取得方法**:
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを選択または作成
3. 「IAM と管理」→「サービスアカウント」を開く
4. サービスアカウントを作成（または既存のものを使用）
5. 「キー」タブから「鍵を追加」→「新しい鍵を作成」→「JSON」を選択
6. ダウンロードしたJSONファイルを`project/`ディレクトリに配置（例: `google-credentials.json`）

**設定方法**:

`.env`ファイルに以下を追加（相対パスまたは絶対パス）：

```env
# 相対パス（推奨）
GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json

# 絶対パス
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/google-credentials.json
```

**Pythonコードでの使用例**:

```python
from vertexai.preview.generative_models import GenerativeModel

# GOOGLE_APPLICATION_CREDENTIALS環境変数が自動的に使用されます
model = GenerativeModel("gemini-pro")
response = model.generate_content("こんにちは")
print(response.text)
```

**必要なPythonパッケージ**:

```bash
pip install google-cloud-aiplatform
```

または`requirements.txt`に追加：

```
google-cloud-aiplatform
```

**注意事項**:
- クレデンシャルファイル（`google-credentials.json`など）は`.gitignore`に含まれているため、Gitにコミットされません
- クレデンシャルファイルは絶対に公開しないでください

## Google AI StudioとVertex AIの使い分け

| 項目 | Google AI Studio | Vertex AI |
|------|------------------|-----------|
| **認証方法** | APIキー（`GOOGLE_API_KEY`） | サービスアカウント（`GOOGLE_APPLICATION_CREDENTIALS`） |
| **用途** | 個人開発、プロトタイピング | 本番環境、エンタープライズ |
| **料金** | 無料枠あり、従量課金 | 従量課金 |
| **機能** | 基本的なGemini API | 高度な機能、カスタマイズ、データセキュリティ |
| **設定の簡単さ** | 簡単（APIキーのみ） | やや複雑（GCPプロジェクト、サービスアカウント設定が必要） |

**推奨**:
- **開発・テスト環境**: Google AI Studio（`GOOGLE_API_KEY`）
- **本番環境**: Vertex AI（`GOOGLE_APPLICATION_CREDENTIALS`）

## サンプルコード

### テキスト生成

```python
import os
import google.generativeai as genai

# APIキーを設定
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# モデルを使用
model = genai.GenerativeModel('gemini-pro')

# テキスト生成
response = model.generate_content("Djangoの利点を3つ教えてください")
print(response.text)
```

### チャット機能

```python
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# チャットを開始
response = chat.send_message("こんにちは")
print(response.text)

# 続けて会話
response = chat.send_message("Pythonについて教えてください")
print(response.text)
```

### 画像を含む入力（Gemini Pro Vision）

```python
import os
from pathlib import Path
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro-vision')

# 画像ファイルを読み込む
image_path = Path('path/to/image.jpg')
with open(image_path, 'rb') as f:
    image_data = f.read()

# 画像とテキストを一緒に送信
response = model.generate_content([
    "この画像に何が写っていますか？",
    {'mime_type': 'image/jpeg', 'data': image_data}
])
print(response.text)
```

### Djangoビューでの使用例

```python
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import os
import google.generativeai as genai

# APIキーを設定（settings.pyで設定することも可能）
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

@require_http_methods(["GET", "POST"])
def chat_view(request):
    response_text = None

    if request.method == "POST":
        user_message = request.POST.get('message', '')

        if user_message:
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(user_message)
                response_text = response.text
            except Exception as e:
                response_text = f"エラーが発生しました: {str(e)}"

    return render(request, 'chat.html', {
        'response_text': response_text
    })
```

## トラブルシューティング

### APIキーが無効というエラーが出る

- APIキーが正しく設定されているか確認してください
- `.env`ファイルが正しく読み込まれているか確認してください
- Google AI StudioでAPIキーが有効化されているか確認してください

### モジュールが見つからないというエラーが出る

必要なパッケージがインストールされているか確認してください：

```bash
# Linux/macOS
venv/bin/pip install google-generativeai

# Windows (Git Bash)
venv/Scripts/pip.exe install google-generativeai
```

### レート制限エラーが出る

無料枠の制限に達した可能性があります。少し時間を置いてから再試行するか、有料プランへのアップグレードを検討してください。

## 参考リンク

- [Google AI Studio](https://aistudio.google.com/)
- [Google AI Python SDK ドキュメント](https://ai.google.dev/tutorials/python_quickstart)
- [Vertex AI ドキュメント](https://cloud.google.com/vertex-ai/docs)
