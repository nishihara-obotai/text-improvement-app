# カスタマイズガイド

このドキュメントでは、プロジェクトの各種設定をカスタマイズする方法を説明します。

## サイト名のカスタマイズ

アプリ名を変更する場合は、`config/settings.py`の`SITE_NAME`を変更してください：

```python
# Site Settings
# サイト名（全テンプレートから{{ SITE_NAME }}で参照可能）
SITE_NAME = "Django App"  # ← ここを変更してアプリ名をカスタマイズ
```

この値は、全テンプレートから`{{ SITE_NAME }}`で参照できます：
- ページタイトル（`<title>`タグ）
- サイドバーのタイトル
- フッターのコピーライト表記
- モバイルヘッダーのタイトル

### 変更例

```python
SITE_NAME = "在庫管理システム"
```

これだけで、全ページのタイトル・ロゴ・フッターが「在庫管理システム」に変更されます。

## テンプレートのカスタマイズ

### ベーステンプレートの構成

プロジェクトには以下のベーステンプレートが用意されています：

#### 1. base.html（プレーンな基本テンプレート）
- TailwindCSS v4（CDN版）の読み込み
- ビジネス向けの配色設定（紫色を避けた落ち着いた色合い）
- Djangoメッセージフレームワーク対応
- サイドバーなしのシンプルなレイアウト
- 用途：ログインページ、エラーページ、ランディングページなど

#### 2. base_sidebar.html（サイドバーありテンプレート）
- base.htmlを継承
- 左側にサイドバーナビゲーション
- レスポンシブデザイン（モバイル対応、CSSのみでメニュー開閉）
- 用途：ダッシュボード、データ一覧ページ、通常のアプリページなど

### 使用方法

#### プレーンなページの場合、`base.html`を継承

```django
{% extends "base.html" %}

{% block title %}ログイン{% endblock %}

{% block content %}
<div class="max-w-md mx-auto mt-8 bg-white rounded shadow-sm p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">ログイン</h2>
    <!-- ログインフォーム -->
</div>
{% endblock %}
```

#### サイドバーが必要なページの場合、`base_sidebar.html`を継承

```django
{% extends "base_sidebar.html" %}

{% block title %}ダッシュボード{% endblock %}

{% block navigation %}
<li>
    <a href="/" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded transition">
        ホーム
    </a>
</li>
<li>
    <a href="/dashboard/" class="block px-4 py-2 text-gray-700 bg-gray-100 rounded transition">
        ダッシュボード
    </a>
</li>
{% endblock %}

{% block content %}
<div class="bg-white rounded shadow-sm p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">ダッシュボード</h2>
    <!-- コンテンツ -->
</div>
{% endblock %}
```

### カスタマイズ可能なブロック

- `{% block title %}`: ページタイトル
- `{% block content %}`: メインコンテンツ
- `{% block navigation %}`: サイドバーメニュー項目（base_sidebar.htmlのみ）
- `{% block page_header %}`: ページヘッダー
- `{% block extra_css %}`: 追加のCSS
- `{% block extra_js %}`: 追加のJavaScript

### カスタムカラーの定義

`base.html`では、TailwindCSSの`@theme`ディレクティブでカスタムカラーを定義しています：

```html
<style type="text/tailwindcss">
  @theme {
    --color-primary-50: oklch(0.97 0.01 240);
    --color-primary-100: oklch(0.93 0.03 240);
    --color-primary-200: oklch(0.86 0.06 240);
    /* ... */
    --color-accent-500: oklch(0.65 0.15 165);
    /* ... */
  }
</style>
```

これらの色は、以下のように使用できます：
- `bg-primary-500`: プライマリカラーの背景
- `text-primary-600`: プライマリカラーのテキスト
- `border-accent-400`: アクセントカラーのボーダー

## 静的ファイルの管理

### 開発環境

`project/assets/`フォルダに静的ファイル（CSS、JavaScript、画像など）を配置します。

開発サーバーでは、自動的に静的ファイルが配信されます（`DEBUG=True`の場合）。

### 本番環境

本番環境では、`collectstatic`コマンドで静的ファイルを収集します：

```bash
python manage.py collectstatic
```

このコマンドは、各アプリの静的ファイルを`STATIC_ROOT`（`project/staticfiles/`）に集約します。

WhiteNoiseが自動的にこれらのファイルを配信します。

## 環境変数のカスタマイズ

`.env`ファイルで環境変数を管理します。主な設定項目：

### データベース設定

```env
# SQLite（デフォルト）
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL（本番環境）
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### デバッグモード

```env
# 開発環境
DEBUG=True

# 本番環境
DEBUG=False
```

### 許可されたホスト

```env
# 開発環境
ALLOWED_HOSTS=localhost,127.0.0.1

# 本番環境
ALLOWED_HOSTS=example.com,www.example.com
```

### Google AI / GCPサービス設定

Gemini APIやGCPサービスを使用する場合は、**[Gemini API利用ガイド](gemini-setup.md)**を参照してください。

以下の環境変数を設定できます：
- `GOOGLE_API_KEY`: Google AI StudioのAPIキー（開発・テスト環境向け）
- `GOOGLE_APPLICATION_CREDENTIALS`: GCP Vertex AIのクレデンシャルファイルパス（本番環境向け）

## アプリケーションの追加

新しいDjangoアプリを追加する場合：

```bash
cd project
python manage.py startapp アプリ名
```

**重要**: `startapp`コマンドは、カレントディレクトリにアプリフォルダを作成するため、必ず`project`ディレクトリに移動してから実行してください。

その後、`config/settings.py`の`INSTALLED_APPS`にアプリを追加：

```python
INSTALLED_APPS = [
    # ...
    'アプリ名',
]
```

## テンプレートディレクトリの構成

テンプレートファイルは、`project/templates/`に集約します：

```
project/templates/
├── base.html              # ベーステンプレート
├── base_sidebar.html      # サイドバー付きベーステンプレート
├── home.html              # トップページ
├── myapp/                 # アプリごとのテンプレート
│   ├── list.html
│   └── detail.html
└── registration/          # 認証関連テンプレート
    ├── login.html
    └── password_reset.html
```

アプリごとにテンプレートを分けたい場合は、`templates/アプリ名/`というディレクトリ構造を使用します。
