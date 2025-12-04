# Django App Template

生成AIで効率的にDjangoアプリを開発するためのテンプレートプロジェクトです。
初心者向けに、構成を極力シンプルに保っています。

## 必要なソフトウェア

開発を始める前に、以下のソフトウェアをインストールしてください。

### 必須

- **Python 3.13**
  - [公式サイト](https://www.python.org/downloads/)からダウンロード
  - インストール後、ターミナルで `python --version` または `python3 --version` で確認

### 推奨（生成AI開発の場合）

- **Visual Studio Code (VSCode)**
  - [公式サイト](https://code.visualstudio.com/)からダウンロード
  - 軽量で拡張性の高いコードエディター

- **Claude Code拡張機能**
  - VSCodeのマーケットプレイスから「Claude Code」をインストール
  - または、VSCodeでこのプロジェクトを開くと自動的に推奨される
  - Anthropic公式のAI開発支援ツール

### オプション

- **Git**
  - [公式サイト](https://git-scm.com/)からダウンロード
  - バージョン管理を行う場合に必要

## クイックスタート

### 生成AIを使用する場合（推奨）

**Claude Code拡張機能を使えば、たった1コマンドですぐに開発を始められます！**

#### 1. テンプレートを展開

ダウンロードしたzipファイルを任意のフォルダに解凍してください。

#### 2. VSCodeでプロジェクトを開く

解凍したフォルダをVSCodeで開きます：
- VSCodeのメニューから「ファイル」→「フォルダーを開く」
- または、解凍したフォルダを右クリック→「Codeで開く」

#### 3. Claude Code拡張機能をインストール（初回のみ）

VSCodeを開くと、推奨拡張機能のインストールを促す通知が表示されます。
「Claude Code」拡張機能をインストールしてください。

#### 4. Claude Codeを起動

VSCodeのターミナルで以下のコマンドを実行：
```bash
claude
```

または、VSCode左下の「Claude Code」アイコンをクリック

#### 5. 初期セットアップを実行

Claude Codeのチャット画面で以下のように入力：
```
初期セットアップ
```

生成AIが以下を**全て自動的に実行**します：
- ✅ 仮想環境（venv）の確認・作成
- ✅ 依存モジュールのインストール
- ✅ `.env`ファイルの作成（SECRET_KEY自動生成）
- ✅ データベースマイグレーション

#### 6. 開発サーバーを起動

以下のいずれかの方法で起動できます：

**方法1: VSCodeのデバッグ機能を使う（推奨）**
- `F5`キーを押す、または
- メニューの「実行」→「デバッグの開始」を選択
- ブレークポイントを使ったデバッグも可能

**方法2: コマンドで起動**
```bash
# Linux/macOS
venv/bin/python project/manage.py runserver

# Windows (PowerShell)
venv\Scripts\python.exe project\manage.py runserver
```

#### 7. ブラウザでアクセス

http://127.0.0.1:8000/

#### 8. スーパーユーザーの作成（管理画面を使う場合）

管理画面（ http://127.0.0.1:8000/admin/ ）を使用する場合は、スーパーユーザーを作成してください：

**方法1: VSCodeタスクで実行（推奨）**
1. `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`) でコマンドパレットを開く
2. 「Tasks: Run Task」を選択
3. 「Django: createsuperuser」を選択

**方法2: コマンドで実行**
```bash
# Linux/macOS
venv/bin/python project/manage.py createsuperuser

# Windows (PowerShell)
venv\Scripts\python.exe project\manage.py createsuperuser
```

作成後、 http://127.0.0.1:8000/admin/ にアクセスしてログインできます。

**完了です！** zipをダウンロードしてVSCodeで開き、「初期セットアップ」と入力するだけで開発を始められます。

> **ポイント**: 仮想環境（venv）が存在しない場合、生成AIが自動的に作成してくれます。手動でvenvを作成する必要はありません。

### 手動でセットアップする場合

<details>
<summary>手動セットアップ手順を表示</summary>

#### 1. 仮想環境の作成と有効化
```bash
python3.13 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows (PowerShell)
```

#### 2. 依存モジュールのインストール
```bash
pip install -r requirements.txt
```

#### 3. 環境変数ファイルの作成
```bash
# Linux/macOS
cd project
cp example.env .env

# Windows (PowerShell)
cd project
copy example.env .env
```

SECRET_KEYを生成：
```bash
# Linux/macOS
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Windows (PowerShell)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

生成されたキーを`.env`ファイルの`SECRET_KEY`に設定してください。

#### 4. データベースマイグレーション
```bash
python manage.py migrate
```

#### 5. 開発サーバーの起動

以下のいずれかの方法で起動できます：

**方法1: VSCodeのデバッグ機能を使う（推奨）**
- `F5`キーを押す、または
- メニューの「実行」→「デバッグの開始」を選択
- ブレークポイントを使ったデバッグも可能

**方法2: コマンドで起動**
```bash
python manage.py runserver
```

ブラウザで http://127.0.0.1:8000/ にアクセスしてください。

#### 6. スーパーユーザーの作成（管理画面を使う場合）

管理画面（ http://127.0.0.1:8000/admin/ ）を使用する場合は、スーパーユーザーを作成してください：

**方法1: VSCodeタスクで実行（推奨）**
1. `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`) でコマンドパレットを開く
2. 「Tasks: Run Task」を選択
3. 「Django: createsuperuser」を選択

**方法2: コマンドで実行**
```bash
python manage.py createsuperuser
```

作成後、 http://127.0.0.1:8000/admin/ にアクセスしてログインできます。

</details>

## 技術スタック

- **Python**: 3.13
- **Django**: 5.2
- **データベース**: SQLite3（開発）/ PostgreSQL（本番）
- **CSS**: TailwindCSS v4 + daisyUI v5（CDN版）
- **静的ファイル配信**: WhiteNoise

### 主要モジュール
- `django-environ`: 環境変数管理
- `whitenoise`: 静的ファイル配信
- `django-debug-toolbar`: 開発時デバッグ
- `ruff`: コードフォーマッター・リンター

### フロントエンド
- **TailwindCSS v4**: ユーティリティファーストCSSフレームワーク
- **daisyUI v5**: TailwindCSSベースのコンポーネントライブラリ
  - ボタン、カード、モーダル、テーブルなど豊富なコンポーネント
  - 公式ドキュメント: https://daisyui.com/components/

## VSCode推奨拡張機能

このプロジェクトでは、以下のVSCode拡張機能を推奨しています（`.vscode/extensions.json`に設定済み）：

- **Python** (`ms-python.python`): Python言語サポート
- **Claude Code** (`anthropic.claude-code`): Anthropic公式のAI開発支援ツール
- **Django** (`batisteo.vscode-django`): Djangoテンプレートのシンタックスハイライト
- **SQLite Viewer** (`alexcvzz.vscode-sqlite`): SQLiteデータベースの閲覧

VSCodeでプロジェクトを開くと、これらの拡張機能のインストールを推奨する通知が表示されます。

## プロジェクト構成

```
project/
├── manage.py              # Django管理コマンド
├── config/                # Django設定
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/             # テンプレートファイル
│   └── base.html         # ベーステンプレート
├── assets/                # 静的ファイル
├── example.env            # 環境変数テンプレート
└── .env                   # 環境変数（自分で作成）
```

## 主な機能

### ベーステンプレート（base.html）

`templates/base.html`がベーステンプレートとして用意されています：

- TailwindCSS v4 + daisyUI v5の読み込み済み
- 左サイドバーナビゲーション
- レスポンシブデザイン（モバイル対応）
- Djangoメッセージフレームワーク対応
- ビジネス向けの落ち着いた配色

新しいページを作成する際は、`base.html`を継承してください：

```django
{% extends "base.html" %}

{% block title %}ページタイトル{% endblock %}

{% block content %}
<!-- daisyUIのカードコンポーネントを使用 -->
<div class="card bg-base-100 shadow-xl">
    <div class="card-body">
        <h2 class="card-title">見出し</h2>
        <p>コンテンツ</p>
        <div class="card-actions justify-end">
            <button class="btn btn-primary">ボタン</button>
        </div>
    </div>
</div>
{% endblock %}
```

## UIデザイン方針

このテンプレートは、ビジネス向けアプリケーション開発を想定しています：

### 色・スタイル
- **紫色を避けた落ち着いた配色**
  - メインカラー: ブルー系（`primary`）
  - 差し色: エメラルド系（`accent`）
- **グラデーションの多用を避ける** - 単色またはシンプルな配色を基本とする
- **ボタン等は境界線をはっきりさせる** - 視認性を重視
- **控えめな角丸でビジネス寄りのデザイン**

### レイアウト
- **左サイドバーでコンテンツ領域を広く確保**
- **レスポンシブデザイン（スマートフォン対応）**

### その他
- **過度な絵文字を避けたシンプルなUI**

## 開発の進め方

### Djangoアプリの追加

```bash
cd project
python manage.py startapp アプリ名
```

**注意**: `startapp`コマンドは、カレントディレクトリにアプリフォルダを作成するため、必ず`project`ディレクトリに移動してから実行してください。

その後、`config/settings.py`の`INSTALLED_APPS`にアプリを追加してください。

### 管理画面の利用

スーパーユーザーを作成：

**方法1: VSCodeタスクで実行（推奨）**
1. `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`) でコマンドパレットを開く
2. 「Tasks: Run Task」を選択
3. 「Django: createsuperuser」を選択

**方法2: コマンドで実行**
```bash
# Linux/macOS
venv/bin/python project/manage.py createsuperuser

# Windows (PowerShell)
venv\Scripts\python.exe project\manage.py createsuperuser
```

作成後、 http://127.0.0.1:8000/admin/ にアクセスしてログインできます。

### 静的ファイルの配信

本番環境では以下を実行：
```bash
# Linux/macOS
venv/bin/python project/manage.py collectstatic

# Windows (PowerShell)
venv\Scripts\python.exe project\manage.py collectstatic
```

開発環境では自動的に配信されます（DEBUG=True時）。

## さらに詳しく

詳細な開発ガイドラインやAI向けの指示は、`CLAUDE.md`を参照してください：

- 「初期セットアップ」コマンドの詳細
- base.htmlの詳細な使い方
- UIデザインガイドライン
- 開発時の注意事項
- トラブルシューティング

## トラブルシューティング

### `.env`ファイルが見つからない

生成AIに「初期セットアップ」と入力してください。自動的に作成されます。

手動で作成する場合：
```bash
# Linux/macOS
cd project
cp example.env .env

# Windows (PowerShell)
cd project
copy example.env .env
```

### データベースをリセットしたい

```bash
# Linux/macOS
rm project/db.sqlite3
venv/bin/python project/manage.py migrate

# Windows (PowerShell)
del project\db.sqlite3
venv\Scripts\python.exe project\manage.py migrate
```

### 静的ファイルが表示されない

開発サーバーでは`DEBUG=True`になっていることを確認してください。
`.env`ファイルを確認：
```
DEBUG=True
```

## ライセンス

このテンプレートのライセンスについては、`LICENSE.txt`を参照してください。

## サポート

### 質問・サポートが必要な場合

- **Claude Codeで質問**: VSCodeでClaude Codeを起動して、わからないことを直接質問してください
- **Slackで質問**: コミュニティのSlackチャンネルで質問や相談ができます

詳細な開発ガイドラインは`CLAUDE.md`を参照してください。
