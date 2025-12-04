# 初期セットアップガイド

このドキュメントは、**Claude（生成AI）向けの実装ガイド**です。ユーザーが「初期セットアップ」と入力した場合、Claudeがこのガイドに従って自動的にセットアップを実行します。

**重要**: すべてのコマンドは**Git Bash**を前提としています（Claude CodeのBashツールはbashシェルを使用するため）。

## 目次

- [クイックスタート（生成AI使用時）](#クイックスタート生成ai使用時)
- [生成AI向け実装ガイド](#生成ai向け実装ガイド)

## クイックスタート（生成AI使用時）

ユーザーが以下のように入力した場合、初期セットアップを自動的に実行します：

```
初期セットアップ
```

生成AIが以下を自動的に実行します：
1. 仮想環境の確認・作成
2. 依存モジュールのインストール
3. `.env`ファイルの作成（SECRET_KEY自動生成）
4. データベースマイグレーション

詳細な実装手順は、[生成AI向け実装ガイド](#生成ai向け実装ガイド)を参照してください。

---

## 生成AI向け実装ガイド

以下は、生成AIが「初期セットアップ」コマンドを実装する際のガイドラインです。

### 「初期セットアップ」コマンドの実装

ユーザーが「**初期セットアップ**」と入力した場合、以下の手順を自動的に実行してください：

#### ステップ1: Python環境の自動検出・作成・使用

**仮想環境の自動管理方針**:

生成AIは以下の順序で自動的に仮想環境を検出・作成・使用します：

1. **venvフォルダの存在確認**
   ```bash
   ls venv
   ```
   - venvフォルダが存在する場合：そのvenv内のpythonを使用
     - Linux/macOS: `venv/bin/python`
     - Windows (Git Bash): `venv/Scripts/python.exe`

   - venvフォルダが存在しない場合：自動的に作成
     - Linux/macOS:
       ```bash
       python3.13 -m venv venv
       ```
     - Windows (Git Bash):
       ```bash
       py -3.13 -m venv venv
       ```
     作成後、そのvenv内のpythonを使用

**重要な実装ルール**:
- Bashツールで`source venv/bin/activate`は使用しない（セッション間で永続化されないため）
- 代わりに、venv内のpythonを直接パス指定で使用する
- **`cd`コマンドを使わず、ルートディレクトリから相対パスで実行する**
  - 良い例: `venv/bin/python project/manage.py migrate`
  - 悪い例: `cd project && python manage.py migrate`（cdはセッション間で永続化されない）
- 例：
  - `venv/bin/python project/manage.py migrate` (Linux/macOS)
  - `venv/Scripts/python.exe project/manage.py migrate` (Windows/Git Bash)
  - `venv/bin/pip install -r requirements.txt` (Linux/macOS)
  - `venv/Scripts/pip.exe install -r requirements.txt` (Windows/Git Bash)

#### ステップ2: 依存モジュールのインストール確認

使用するpythonのパスに応じて、以下のコマンドでDjangoのインストール状況を確認：
- venv内のpythonを使用する場合（Linux/macOS）：`venv/bin/pip list | grep Django`
- venv内のpythonを使用する場合（Windows/Git Bash）：`venv/Scripts/pip.exe list | findstr Django`

Djangoがインストールされていない場合：
- venv内のpipを使用する場合（Linux/macOS）：`venv/bin/pip install -r requirements.txt`
- venv内のpipを使用する場合（Windows/Git Bash）：`venv/Scripts/pip.exe install -r requirements.txt`

#### ステップ3: `.env`ファイルの作成

**3-1. 存在確認**
```bash
ls project/.env
```

**3-2. `.env`ファイルが存在しない場合のみ以下を実行**

a. `example.env`を`.env`にコピー：
```bash
cp project/example.env project/.env
```

b. SECRET_KEYを生成（使用するpythonのパスに応じて）：
- venv内のpythonを使用する場合（Linux/macOS）：
  ```bash
  venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- venv内のpythonを使用する場合（Windows/Git Bash）：
  ```bash
  venv/Scripts/python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

c. 生成したSECRET_KEYで`.env`ファイルの`SECRET_KEY`行を置き換え

**3-3. `.env`ファイルが既に存在する場合**

スキップして次のステップへ

#### ステップ4: データベースマイグレーション

使用するpythonのパスに応じて、以下のコマンドを実行：

cdを使わず、ルートディレクトリから相対パスで実行：

- venv内のpythonを使用する場合（Linux/macOS）：
  ```bash
  venv/bin/python project/manage.py migrate
  ```
- venv内のpythonを使用する場合（Windows/Git Bash）：
  ```bash
  venv/Scripts/python.exe project/manage.py migrate
  ```

#### ステップ5: 完了メッセージ

以下のメッセージをユーザーに表示（使用したpython環境に応じて適切なコマンドを表示）：

```
初期セットアップが完了しました！

【開発サーバーの起動】
VSCodeのデバッグ機能を使用してください：
- F5キーを押す、または
- メニューの「実行」→「デバッグの開始」を選択
ブレークポイントを使ったデバッグも可能です。

ブラウザで http://127.0.0.1:8000/ にアクセスしてください。

【スーパーユーザーの作成】
管理画面を使用する場合は、VSCodeタスクでスーパーユーザーを作成してください：
- Ctrl+Shift+P (macOS: Cmd+Shift+P) でコマンドパレットを開く
- 「Tasks: Run Task」を選択
- 「Django: createsuperuser」を選択

作成後、 http://127.0.0.1:8000/admin/ にアクセスしてログインできます。
```
