# トラブルシューティング

Djangoアプリ開発中によくある問題とその解決方法をまとめています。

## マイグレーション関連

### マイグレーションエラー

モデルを変更した後にマイグレーションエラーが発生した場合：

#### 方法1: マイグレーションをリセット（開発初期のみ）

```bash
# データベースをリセット
rm db.sqlite3

# マイグレーションファイルを削除（__init__.pyは残す）
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# マイグレーションを再作成
python manage.py makemigrations
python manage.py migrate

# スーパーユーザーを再作成
python manage.py createsuperuser
```

**警告**: この方法は全てのデータが失われるため、開発初期のみ使用してください。

#### 方法2: 特定のアプリのマイグレーションをリセット

```bash
# マイグレーションをゼロに戻す（データは保持）
python manage.py migrate app_name zero

# 再度マイグレーション
python manage.py migrate app_name
```

#### 方法3: フェイクマイグレーション

```bash
# マイグレーションを実行したことにする（データベースは変更しない）
python manage.py migrate --fake app_name

# マイグレーションファイルを削除
rm app_name/migrations/0002_*.py

# マイグレーションを再作成
python manage.py makemigrations
python manage.py migrate
```

### "No changes detected" と表示される

モデルを変更したのに`makemigrations`で変更が検出されない場合：

1. **アプリがINSTALLED_APPSに登録されているか確認**
   ```python
   # config/settings.py
   INSTALLED_APPS = [
       # ...
       'your_app_name',  # ← 登録されているか確認
   ]
   ```

2. **アプリ名を明示的に指定**
   ```bash
   python manage.py makemigrations your_app_name
   ```

## 静的ファイル関連

### 静的ファイルが表示されない

#### 開発環境の場合

1. **DEBUGモードを確認**
   ```python
   # .env
   DEBUG=True
   ```

2. **STATIC_URLを確認**
   ```python
   # config/settings.py
   STATIC_URL = '/static/'
   ```

3. **テンプレートでload staticを使用**
   ```django
   {% load static %}
   <img src="{% static 'images/logo.png' %}">
   ```

#### 本番環境の場合

1. **collectstaticを実行**
   ```bash
   python manage.py collectstatic
   ```

2. **WhiteNoiseの設定を確認**
   ```python
   # config/settings.py
   MIDDLEWARE = [
       # ...
       'whitenoise.middleware.WhiteNoiseMiddleware',
       # ...
   ]
   ```

### CSSやJavaScriptの変更が反映されない

ブラウザのキャッシュが原因の場合：

- **ハードリロード**: `Ctrl + Shift + R` (Windows) または `Cmd + Shift + R` (Mac)
- **キャッシュクリア**: ブラウザの設定からキャッシュをクリア

## データベース関連

### データベースをリセットしたい

#### SQLiteの場合

```bash
# データベースファイルを削除
rm project/db.sqlite3

# マイグレーション実行
python manage.py migrate

# スーパーユーザー作成
python manage.py createsuperuser
```

#### PostgreSQLの場合

```bash
# データベースを削除して再作成
dropdb your_database_name
createdb your_database_name

# マイグレーション実行
python manage.py migrate

# スーパーユーザー作成
python manage.py createsuperuser
```

### "database is locked" エラー（SQLite）

開発サーバーやシェルを複数起動している場合に発生します：

1. **全てのDjangoプロセスを停止**
2. **データベースファイルのロックを解除**
   ```bash
   # Linuxの場合
   fuser -k db.sqlite3

   # または単純に再起動
   ```

## 認証関連

### 管理画面にログインできない

1. **スーパーユーザーを作成**
   ```bash
   python manage.py createsuperuser
   ```

2. **パスワードをリセット**
   ```bash
   python manage.py changepassword username
   ```

### ログイン後にリダイレクトされない

`LOGIN_REDIRECT_URL`を設定：

```python
# config/settings.py
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
```

## 環境変数関連

### .envファイルが読み込まれない

1. **ファイルの場所を確認**
   ```bash
   ls project/.env
   ```

2. **django-environがインストールされているか確認**
   ```bash
   pip list | grep django-environ
   ```

3. **settings.pyで正しく読み込んでいるか確認**
   ```python
   import environ
   env = environ.Env()
   environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
   ```

### SECRET_KEYエラー

`.env`ファイルに`SECRET_KEY`が設定されているか確認：

```bash
# SECRET_KEYを生成
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

生成されたキーを`.env`に設定：

```env
SECRET_KEY=生成されたキー
```

## テンプレート関連

### テンプレートが見つからない（TemplateDoesNotExist）

1. **テンプレートの場所を確認**
   - テンプレートは`project/templates/`に配置
   - アプリごとに分ける場合は`project/templates/app_name/`

2. **settings.pyのTEMPLATES設定を確認**
   ```python
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [BASE_DIR / 'templates'],  # ← 設定されているか確認
           # ...
       },
   ]
   ```

### テンプレート変数が表示されない

1. **コンテキストに変数を渡しているか確認**
   ```python
   return render(request, 'template.html', {'variable': value})
   ```

2. **テンプレートで正しく参照しているか確認**
   ```django
   {{ variable }}  <!-- 正しい -->
   {{ variable }}  <!-- スペルミス -->
   ```

## パフォーマンス関連

### ページの読み込みが遅い

#### N+1問題の確認

```python
# 悪い例（N+1問題）
books = Book.objects.all()
for book in books:
    print(book.author.name)  # ← 各ループでクエリ発行

# 良い例（select_related使用）
books = Book.objects.select_related('author').all()
for book in books:
    print(book.author.name)  # ← 1回のクエリで取得
```

#### Django Debug Toolbarで確認

開発環境では、Debug Toolbarでクエリ数を確認できます：

```python
# config/settings.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

## その他の問題

### ModuleNotFoundError

パッケージがインストールされていない場合：

```bash
pip install -r requirements.txt
```

### "Port is already in use" エラー

ポート8000が既に使用されている場合：

```bash
# 別のポートで起動
python manage.py runserver 8001

# または既存のプロセスを終了
# Linuxの場合
lsof -ti:8000 | xargs kill -9

# Windowsの場合
netstat -ano | findstr :8000
taskkill /PID プロセスID /F
```

### CSRF検証エラー

フォーム送信時にCSRFエラーが発生する場合：

```django
<form method="post">
    {% csrf_token %}  <!-- ← 必須 -->
    <!-- フォームフィールド -->
</form>
```

## VSCodeデバッグ関連

### デバッグが起動しない

VSCodeでF5キーを押してもデバッグが起動しない、またはエラーが発生する場合：

#### 1. Pythonインタープリターを確認

VSCodeで正しいPythonインタープリター（仮想環境のPython）が選択されているか確認：

1. `Ctrl + Shift + P`（macOS: `Cmd + Shift + P`）
2. 「Python: Select Interpreter」を選択
3. `./venv/bin/python`（Windows/Git Bash: `./venv/Scripts/python.exe`）を選択

#### 2. debugpyがインストールされているか確認

```bash
# 仮想環境がアクティブな場合
pip list | grep debugpy

# Linux/macOS（venv内のpipを使用）
venv/bin/pip list | grep debugpy

# Windows/Git Bash（venv内のpipを使用）
venv/Scripts/pip.exe list | findstr debugpy
```

debugpyがインストールされていない場合：

```bash
# 仮想環境がアクティブな場合
pip install debugpy

# Linux/macOS（venv内のpipを使用）
venv/bin/pip install debugpy

# Windows/Git Bash（venv内のpipを使用）
venv/Scripts/pip.exe install debugpy
```

#### 3. launch.jsonの設定を確認

`.vscode/launch.json`が存在し、正しい設定になっているか確認：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django: runserver",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/project/manage.py",
      "args": ["runserver"],
      "django": true,
      "python": "${command:python.interpreterPath}",
      "cwd": "${workspaceFolder}/project",
      "console": "integratedTerminal"
    }
  ]
}
```

#### 4. Python拡張機能がインストールされているか確認

VSCodeの拡張機能タブで「Python」（Microsoft製）がインストールされているか確認してください。

#### 5. ワークスペースフォルダを確認

VSCodeで正しいフォルダ（プロジェクトのルートディレクトリ）を開いているか確認してください。

### ブレークポイントが無視される

ブレークポイントを設定しても止まらない場合：

1. **justMyCodeをfalseに設定**

   `.vscode/launch.json`の該当する設定で：
   ```json
   "justMyCode": false
   ```

2. **ブレークポイントが正しい場所に設定されているか確認**

   - コメント行や空白行には設定できません
   - 実際に実行されるコード行に設定してください

3. **条件付きブレークポイントを試す**

   ブレークポイントを右クリックして「条件付きブレークポイントを編集」を選択

### デバッグコンソールでエラーが表示される

```
debugpy.server: Timed out waiting for debug adapter to connect
```

このエラーが表示される場合：

1. **ファイアウォールの確認**

   ファイアウォールがlocalhostのポート5678をブロックしていないか確認

2. **ポートを変更**

   別のアプリケーションがポート5678を使用している可能性があります。`.vscode/launch.json`に以下を追加：
   ```json
   "debugOptions": ["WaitOnAbnormalExit", "WaitOnNormalExit"],
   "port": 5679
   ```

3. **VSCodeを再起動**

   VSCodeを完全に終了して再起動してください

## さらに詳しく

- [Django公式ドキュメント - FAQ](https://docs.djangoproject.com/en/stable/faq/)
- [Django公式ドキュメント - トラブルシューティング](https://docs.djangoproject.com/en/stable/howto/)
