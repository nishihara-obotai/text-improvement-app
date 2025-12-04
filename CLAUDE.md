# Django プロジェクト - 開発ガイド

このドキュメントは、生成AIでDjangoアプリを開発する際の基本ルールとプロジェクト構成を記載しています。

## プロジェクト概要

生成AIで効率的にDjangoアプリを開発するためのテンプレートプロジェクトです。
初級者向けのバイブコーディング向けに、構成を極力シンプルに保っています。

## ディレクトリ構成

```
project/                        # Djangoプロジェクトのルートフォルダ
├── manage.py                   # Django管理コマンド
├── config/                     # Djangoの設定フォルダ
│   ├── settings.py             # プロジェクト設定（django-environで環境変数管理）
│   ├── urls.py                 # URLルーティング
│   ├── wsgi.py                 # WSGI設定
│   └── asgi.py                 # ASGI設定
├── templates/                  # テンプレートファイル（アプリ配下ではなくここに集約）
│   ├── base.html               # ベーステンプレート
│   └── base_sidebar.html       # サイドバー付きベーステンプレート
├── assets/                     # 静的ファイル（collectstaticの対象）
├── docs/                       # プロジェクトドキュメント（詳細ガイド）
├── example.env                 # 環境変数テンプレート（これをコピーして.envを作成）
├── .env                        # 環境変数（SECRET_KEY、DB接続情報等）※自分で作成
└── db.sqlite3                  # SQLiteデータベース（ローカル開発用、自動生成）
```

## 技術スタック

### Python・Django
- **Python**: 3.13
- **Django**: 5.2
- **必須モジュール**:
  - `django-environ`: 環境変数管理（データベース接続、SECRET_KEY等）
  - `django-import-export`: データインポート・エクスポート（XLSX, CSV, JSON対応）
  - `openpyxl`: XLSX形式のサポート（django-import-export用）
  - `django-debug-toolbar`: 開発時のデバッグ用
  - `ruff`: コードフォーマッター・リンター

### データベース
- **ローカル開発**: SQLite3（.envで設定、デフォルト）
- **本番環境**: PostgreSQL（DATABASE_URL環境変数で設定）

### フロントエンド
- **CSS**: TailwindCSS v4 + daisyUI v5（CDN版）
  - daisyUI v5: `https://cdn.jsdelivr.net/npm/daisyui@5`
  - TailwindCSS v4: `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4`
  - NodeJSを使ったビルドは行わない
  - カスタムカラーは`@theme`ディレクティブで定義（`primary`、`accent`）
  - daisyUIコンポーネントを活用してUI開発を効率化
  - daisyUIの公式ドキュメント: https://daisyui.com/components/
- **JavaScript**: 最小限の利用
  - NodeJSを使ったビルドは行わない
  - 基本的には必要最小限のバニラJSを使用
  - 複雑な機能を実現する場合、CDNホストされたライブラリの利用は許可
    - 例: Chart.js（グラフ描画）、Alpine.js（軽量リアクティブフレームワーク）など

### 静的ファイル配信
- **WhiteNoise**: 本番環境での静的ファイル配信

## セットアップ手順

### クイックスタート（生成AI使用時）

生成AIを使用する場合は、以下の一言で初期セットアップが完了します：

```
初期セットアップ
```

生成AIが以下を自動的に実行します：
1. 仮想環境の確認・作成
2. 依存モジュールのインストール
3. `.env`ファイルの作成（SECRET_KEY自動生成）
4. データベースマイグレーション

### 詳細な手順

手動セットアップやGCPサービスの設定など、詳細な手順については以下のドキュメントを参照してください：

- **[初期セットアップガイド](docs/initial-setup.md)** - 手動セットアップ、GCP設定、AI向け実装ガイド

## 開発方針

### ミドルウェア
- Dockerは使用しない（初級者向けのため構成を簡素化）
- ミドルウェアは最小限に抑える

### シンプルな構成
- NodeJSによるビルドプロセスは使用しない
- TailwindCSSはCDN版を使用
- JavaScriptは最小限に抑える（基本はバニラJS、複雑な機能にはCDNホストされたライブラリ可）

## UIデザイン方針

生成AIがUIコードを生成する際は、以下のデザイン原則に従ってください：

### 色・スタイル
- **生成AIで使いがちな紫色は極力避ける**
- **ビジネス向けで使いやすい落ち着いた色合いを選択**
  - メインカラー: ブルー系（`bg-primary-500`、`text-primary-600`等）
  - 差し色: エメラルド系（`bg-accent-500`、`text-accent-600`等）を1色使用
  - base.htmlで`primary`と`accent`カラーパレットが定義済み
- **グラデーションの多用を避ける**
  - 単色またはシンプルな配色を基本とする
  - 必要な場合のみ控えめなグラデーションを使用（`from-*`、`to-*`クラスの使用は最小限に）
- **ボタン等は境界線をはっきりさせる**
  - `border`、`border-2`クラスを使用して視認性を向上
  - ホバー時の状態変化も明確にする（`hover:border-*`）
  - 例: `<button class="bg-primary-500 text-white border-2 border-primary-600 hover:bg-primary-600">`
- **ボタン等の角丸は大きくしすぎず、ビジネス寄りのデザインを意識**
  - TailwindCSSの`rounded`や`rounded-md`程度に留める
  - `rounded-full`や`rounded-3xl`は避ける

### ボタン・インタラクション設計
- **ボタンは意味的に正しいHTMLタグを使用**
  - フォーム送信やJavaScriptによるアクション: `<button>`タグを使用
  - ページ遷移を伴うリンク: `<a>`タグを使用
  - 悪い例: `<div onclick="...">`（アクセシビリティが低い）
- **マウスホバー時に指先カーソル（cursor: pointer）を表示**
  - TailwindCSSでは`cursor-pointer`クラスを使用
  - ボタンやリンクには必ず適用する
- **ホバー状態のスタイル変化を明確にする**
  - 背景色: `hover:bg-primary-600`
  - ボーダー色: `hover:border-primary-700`
  - 不透明度: `hover:opacity-90`
- **押下状態（active状態）のスタイルを実装**
  - マウスダウンやタッチ時に見た目が変化することで、押せていることを明確にする
  - TailwindCSSでは`active:`プレフィックスを使用
  - 背景色を暗くする: `active:bg-primary-700`
  - 縮小効果: `active:scale-95`
  - 例: `<button class="cursor-pointer bg-primary-500 hover:bg-primary-600 active:bg-primary-700 active:scale-95 transition">`
- **トランジション効果で滑らかな変化を実現**
  - `transition`クラスを使用してスムーズな状態変化を実現
  - 例: `transition duration-150 ease-in-out`
- **daisyUIのbtn-ghostクラスの使用は極力避ける**
  - `btn-ghost`は背景色がなく、視認性が低いためビジネス向けアプリでは推奨しない
  - 代わりに、`btn-primary`、`btn-secondary`、`btn-outline`など、明確な境界線や背景色を持つスタイルを使用
  - 例外: ハンバーガーメニューなど、ごく一部のアイコンボタンのみ使用可

### レイアウト
- **メニューバーは左側に配置**（上下はコンテンツ表示領域が狭くなるため避ける）
- **スマートフォンでの利用も想定したレスポンシブデザインを実装**
  - TailwindCSSのブレークポイント（`sm:`, `md:`, `lg:`等）を活用

### その他
- **過度な絵文字の利用は避ける**
- UI上わかりやすい部分（メニュー等）では絵文字を活用可
- シンプルで直感的なデザインを心がける

## 開発時の注意事項

### テンプレートファイル
- アプリ配下の`templates/`ではなく、**プロジェクト直下の`project/templates/`に集約**
- アプリごとにテンプレートを分けたい場合は、`templates/アプリ名/`というディレクトリ構造を使用

#### ベーステンプレート

**1. base.html（プレーンな基本テンプレート）**
- TailwindCSS v4（CDN版）の読み込み
- ビジネス向けの配色設定（紫色を避けた落ち着いた色合い）
- Djangoメッセージフレームワーク対応
- サイドバーなしのシンプルなレイアウト
- 用途：ログインページ、エラーページ、ランディングページなど

**2. base_sidebar.html（サイドバーありテンプレート）**
- base.htmlを継承
- 左側にサイドバーナビゲーション
- レスポンシブデザイン（モバイル対応、CSSのみでメニュー開閉）
- 用途：ダッシュボード、データ一覧ページ、通常のアプリページなど

### 静的ファイル
- `project/assets/`に静的ファイルを格納
- 本番環境では`collectstatic`コマンドで収集
  ```bash
  # Linux/macOS
  venv/bin/python project/manage.py collectstatic

  # Windows (Git Bash)
  venv/Scripts/python.exe project/manage.py collectstatic
  ```

### 環境変数
- `.env`ファイルで管理（django-environを使用）
- SECRET_KEYやデータベース接続情報などを記載
- **`.env`ファイルは絶対にGitにコミットしない**（.gitignoreに含まれています）

### コードフォーマット
- ruffを使用してコードスタイルを統一
  ```bash
  # Linux/macOS
  venv/bin/ruff check .
  venv/bin/ruff format .

  # Windows (Git Bash)
  venv/Scripts/ruff.exe check .
  venv/Scripts/ruff.exe format .
  ```

## アプリケーションの追加

新しいDjangoアプリを追加する場合:

```bash
cd project
python manage.py startapp アプリ名
```

**重要**: `startapp`コマンドは、カレントディレクトリにアプリフォルダを作成するため、必ず`project`ディレクトリに移動してから実行してください。これは`manage.py`コマンドの中でも例外的な扱いです（他のコマンドは相対パスで実行可能）。

その後、`config/settings.py`の`INSTALLED_APPS`にアプリを追加してください。

## 関連ドキュメント

より詳細な情報は、以下のドキュメントを参照してください：

- **[初期セットアップガイド](docs/initial-setup.md)** - 手動セットアップ、GCP設定、AI向け実装ガイド
- **[推奨Pythonモジュール](docs/recommended-modules.md)** - PDF作成、Excel、QRコード、画像処理など
- **[データインポート・エクスポート](docs/import-export.md)** - django-import-exportの詳細な使い方
- **[カスタマイズガイド](docs/customization.md)** - サイト名、テンプレート、環境変数のカスタマイズ
- **[Gemini API利用ガイド](docs/gemini-setup.md)** - Google AI StudioとVertex AIの設定、サンプルコード
- **[Userモデルの拡張](docs/user-model-extension.md)** - ユーザープロフィールの実装方法
- **[トラブルシューティング](docs/troubleshooting.md)** - よくある問題と解決方法

## 開発ガイドライン（AI向け）

生成AIがコードを生成する際は、以下に従ってください：

### 「初期セットアップ」コマンド

ユーザーが「**初期セットアップ**」と入力した場合、**[初期セットアップガイド](docs/initial-setup.md)を参照して、記載されている手順を自動的に実行してください。**

**重要な構成ルール**：

以下は、初期セットアップを含むすべての開発作業で遵守すべき構成ルールです：

1. **Pythonコマンドの実行方針（クロスプラットフォーム対応）**
   - Bashツールで`source venv/bin/activate`は使用しない（セッション間で永続化されないため）
   - 代わりに、venv内のpythonを直接パス指定で使用する
   - **Linux/macOS**: `venv/bin/python`, `venv/bin/pip`
   - **Windows (Git Bash)**: `venv/Scripts/python.exe`, `venv/Scripts/pip.exe`
   - 例：
     - `venv/bin/python project/manage.py migrate` (Linux/macOS)
     - `venv/Scripts/python.exe project/manage.py migrate` (Windows/Git Bash)

2. **コマンド実行時の原則**
   - **`cd`コマンドを使わず、ルートディレクトリから相対パスで実行する**
   - 良い例（Linux/macOS）: `venv/bin/python project/manage.py migrate`
   - 良い例（Windows/Git Bash）: `venv/Scripts/python.exe project/manage.py migrate`
   - 悪い例: `cd project && python manage.py migrate`（cdはセッション間で永続化されない）
   - **例外**: `startapp`コマンドはカレントディレクトリにアプリフォルダを作成するため、`cd project`してから実行する必要がある

3. **環境変数の管理**
   - `.env`ファイルで管理（django-environを使用）
   - SECRET_KEYやデータベース接続情報などを記載
   - **`.env`ファイルは絶対にGitにコミットしない**（.gitignoreに含まれています）
   - GCPクレデンシャルは相対パスで指定（例: `GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json`）

### プロジェクト開始時の自動確認

ユーザーが「初期セットアップ」と明示的に入力していない場合でも、以下の状況では`.env`ファイルの確認を行ってください：

- **最初のコーディング作業を行う前**
- **Django関連のコマンドを実行する前**（migrate、runserver等）

`.env`ファイルが存在しない場合は、ユーザーに以下のように提案してください：

> `.env`ファイルが見つかりません。初期セットアップを実行しますか？「初期セットアップ」と入力していただくと、自動的にセットアップを行います。

### 必須ルール

1. **UIデザイン方針を厳守**
   - 紫色を避ける
   - 左メニュー配置
   - レスポンシブデザイン
   - ビジネス向けの落ち着いた色合い
   - btn-ghostクラスの使用は極力避ける（視認性が低いため）

2. **テンプレートファイルは`project/templates/`に配置**

3. **base.htmlを活用**
   - `project/templates/base.html`がベーステンプレートとして用意されています
   - 新しいページを作成する際は、必ず`base.html`または`base_sidebar.html`を継承してください
   - TailwindCSS v4 + daisyUI v5は既に読み込まれているため、CDNの追加読み込みは不要です
   - プロジェクト共通のカスタムカラー（primary/accent）が`@theme`ディレクティブで定義済みです

4. **TailwindCSS v4 + daisyUI v5（CDN版）を使用**
   - ビルドプロセスは追加しない
   - `base.html`または`base_sidebar.html`にTailwindCSS v4 + daisyUI v5のCDNが既に読み込まれているため、通常は追加不要
   - daisyUIコンポーネントを積極的に活用してUI開発を効率化
   - daisyUIの公式ドキュメント: https://daisyui.com/components/
   - 利用可能なコンポーネント例：
     - ボタン: `<button class="btn btn-primary">ボタン</button>`
     - カード: `<div class="card bg-base-100 shadow-xl">...</div>`
     - モーダル: `<dialog class="modal">...</dialog>`
     - テーブル: `<table class="table">...</table>`
     - フォーム: `<input type="text" class="input input-bordered" />`
   - 新規にスタンドアロンHTMLを作成する場合は、base.htmlと同じCDNを使用

5. **JavaScriptは最小限**に抑える
   - 基本的にはバニラJSを使用
   - 複雑な機能を実現する場合は、CDNホストされたライブラリの利用を許可
   - ビルドプロセスは不要

6. **トグル動作はCSSのみで実装**
   - ハンバーガーメニュー、モーダル、ドロワー、アコーディオン等のトグル動作は**JavaScriptを使わずCSSのみで実装**
   - チェックボックス（`<input type="checkbox">`）+ `<label>`の組み合わせと`:checked`疑似クラスを活用
   - TailwindCSSの`peer-checked:`、`has()`セレクタなどを活用
   - `pointer-events-none`と`peer-checked:pointer-events-auto`でオーバーレイの制御を忘れずに
   - 実装例: `base_sidebar.html`のハンバーガーメニュー
     ```html
     <!-- チェックボックス（非表示） -->
     <input type="checkbox" id="mobile-menu-toggle" class="peer hidden">

     <!-- トグルボタン -->
     <label for="mobile-menu-toggle" class="cursor-pointer">...</label>

     <!-- トグルされるコンテンツ -->
     <div class="invisible peer-checked:visible pointer-events-none peer-checked:pointer-events-auto">
       ...
     </div>
     ```

7. **シンプルな構成を維持**
   - 不要な複雑さを避ける
   - 初級者でも理解できるコード

8. **バージョン管理の厳守**
   - **Python 3.13を使用**：下位バージョンに変更しない
   - **Django 5.2を使用**：下位バージョンに変更しない
   - **TailwindCSS v4を使用**：v3やそれ以前のバージョンに変更しない
     - CDN URL: `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4`
     - メジャーバージョン4を固定することが重要（`@4`の指定を維持）
   - **daisyUI v5を使用**：v4やそれ以前のバージョンに変更しない
     - CDN URL: `https://cdn.jsdelivr.net/npm/daisyui@5`
     - メジャーバージョン5を固定することが重要（`@5`の指定を維持）
   - **理由**：
     - TailwindCSS v4とdaisyUI v5は、v3/v4から大幅な仕様変更がある
     - base.htmlのスタイル設定は最新バージョンに最適化されている
     - 下位バージョンを使用すると、既存のスタイルが正しく動作しない
     - メジャーバージョンを固定しないと、予期しない破壊的変更が発生する可能性がある

### 推奨事項

- クラスベースビューよりも関数ベースビューを優先（シンプルさ重視）
- 必要に応じてDjangoのジェネリックビューを活用
- URLは分かりやすい名前を付ける
- テンプレートは継承を活用して共通部分を再利用
- **Userモデルを拡張する場合**は、AbstractUserを継承せず、UserProfileモデルをOneToOneFieldで紐づける方法を採用（詳細は`docs/user-model-extension.md`を参照）
- **manage.pyなどを実行する際は、cdを使わずルートディレクトリから相対パスで実行**
  - 推奨（Linux/macOS）: `venv/bin/python project/manage.py runserver`
  - 推奨（Windows/Git Bash）: `venv/Scripts/python.exe project/manage.py runserver`
  - 非推奨: `cd project && python manage.py runserver`（cdはセッション間で永続化されない）
  - **例外**: `startapp`コマンドはカレントディレクトリにアプリフォルダを作成するため、`cd project`してから実行する必要がある

## さらに詳しく

- [Django公式ドキュメント](https://docs.djangoproject.com/)
- [TailwindCSS公式ドキュメント](https://tailwindcss.com/docs)
- [daisyUI公式ドキュメント](https://daisyui.com/)
- [django-environ GitHub](https://github.com/joke2k/django-environ)
