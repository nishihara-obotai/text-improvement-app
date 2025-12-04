# データインポート・エクスポート

このプロジェクトには`django-import-export`が標準で組み込まれており、Django admin画面から簡単にデータのインポート・エクスポートができます。

## 対応フォーマット

- **XLSX** (Excel形式) - openpyxl使用
- **CSV** (カンマ区切り)
- **JSON** (JavaScript Object Notation)

## 基本的な使い方

### 1. モデルに対応したResourceクラスを作成

アプリの`admin.py`にResourceクラスとImportExportModelAdminを定義します：

```python
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import YourModel

class YourModelResource(resources.ModelResource):
    class Meta:
        model = YourModel
        # インポート・エクスポートする項目を指定（省略時は全項目）
        fields = ('id', 'name', 'created_at', 'updated_at')
        # エクスポート時の列の順序を指定
        export_order = ('id', 'name', 'created_at', 'updated_at')

@admin.register(YourModel)
class YourModelAdmin(ImportExportModelAdmin):
    resource_class = YourModelResource
    list_display = ('id', 'name', 'created_at')
```

### 2. Admin画面での操作

管理画面（ `http://127.0.0.1:8000/admin/` ）にアクセスすると、各モデルのリスト画面に以下のボタンが表示されます：

- **インポート**: データをアップロードして取り込み
- **エクスポート**: データをダウンロード

### 3. インポート手順

1. Admin画面で対象モデルを選択
2. 「インポート」ボタンをクリック
3. ファイル形式（XLSX, CSV, JSON）を選択
4. ファイルをアップロード
5. プレビュー画面でデータを確認
6. 「インポート確定」で取り込み

### 4. エクスポート手順

1. Admin画面で対象モデルを選択
2. エクスポートするデータを選択（全件または一部）
3. 「エクスポート」ボタンをクリック
4. ファイル形式を選択してダウンロード

## カスタマイズ例

### インポート時のバリデーション

```python
class YourModelResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        # インポート前のバリデーション
        if not row.get('name'):
            raise ValueError('名前は必須です')

    class Meta:
        model = YourModel
```

### 特定フィールドのみエクスポート

```python
class YourModelResource(resources.ModelResource):
    class Meta:
        model = YourModel
        fields = ('id', 'name')  # idとnameのみ
        exclude = ('password',)  # パスワードを除外
```

### インポート時の重複処理

```python
class YourModelResource(resources.ModelResource):
    class Meta:
        model = YourModel
        import_id_fields = ['id']  # IDで重複判定
        skip_unchanged = True  # 変更がない行はスキップ
        report_skipped = True  # スキップした行を報告
```

### カスタムフィールドの追加

```python
from import_export import fields, resources

class YourModelResource(resources.ModelResource):
    full_name = fields.Field(column_name='フルネーム')

    class Meta:
        model = YourModel
        fields = ('id', 'first_name', 'last_name', 'full_name')
        export_order = ('id', 'full_name', 'first_name', 'last_name')

    def dehydrate_full_name(self, obj):
        # エクスポート時にフルネームを生成
        return f"{obj.last_name} {obj.first_name}"
```

### 外部キーの扱い

```python
class BookResource(resources.ModelResource):
    author_name = fields.Field(
        column_name='著者名',
        attribute='author',
        widget=widgets.ForeignKeyWidget(Author, 'name')
    )

    class Meta:
        model = Book
        fields = ('id', 'title', 'author_name', 'published_date')
```

### 日付フォーマットのカスタマイズ

```python
from import_export import widgets

class YourModelResource(resources.ModelResource):
    created_at = fields.Field(
        column_name='作成日',
        attribute='created_at',
        widget=widgets.DateWidget('%Y年%m月%d日')
    )

    class Meta:
        model = YourModel
```

## 注意事項

- **大量データのインポートはタイムアウトの可能性**があるため、分割して実行してください
- **本番環境ではCSRF対策**が有効になっているため、ログイン必須です
- **データの整合性**を保つため、インポート前に必ずプレビュー確認を行ってください
- **外部キー**や**多対多フィールド**を含む場合は、適切なWidgetを使用してください

## より詳しく

- [django-import-export 公式ドキュメント](https://django-import-export.readthedocs.io/)
