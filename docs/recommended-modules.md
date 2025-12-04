# 推奨Pythonモジュール

アプリに特定の機能を追加する際に推奨するPythonモジュールです。

## PDF作成

### WeasyPrint (`weasyprint`)
- HTMLをPDFに変換
- インストール: `pip install weasyprint`
- 用途: 請求書、レポート、証明書の発行

**使用例**:
```python
from django.http import HttpResponse
from weasyprint import HTML

def generate_pdf(request):
    html_string = render_to_string('invoice.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response
```

## Excelファイル作成

### openpyxl (`openpyxl`)
- .xlsx形式の読み書き、セルのスタイリング対応
- インストール: `pip install openpyxl`
- 用途: データエクスポート、帳票出力
- **注意**: django-import-export用に既にインストール済み

**使用例**:
```python
from openpyxl import Workbook
from django.http import HttpResponse

def export_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "データ一覧"

    # ヘッダー
    ws.append(['ID', '名前', '日付'])

    # データ
    for item in MyModel.objects.all():
        ws.append([item.id, item.name, item.created_at])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
    wb.save(response)
    return response
```

## QRコード生成

### qrcode (`qrcode`)
- QRコードをSVG形式で生成（デフォルト）
- インストール: `pip install qrcode`
- 用途: チケット発行、URL短縮
- **PNG等の画像形式が必要な場合**: `pip install qrcode[pil]` でPillowを追加インストール

**使用例**:
```python
import qrcode
from io import BytesIO
from django.http import HttpResponse

def generate_qr(request):
    # QRコード生成
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data('https://example.com')
    qr.make(fit=True)

    # PNG画像として出力
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')
```

## 画像処理

### Pillow (`Pillow`)
- 画像のリサイズ、回転、フィルタ適用
- インストール: `pip install Pillow`
- 用途: サムネイル生成、画像アップロード処理

**使用例**:
```python
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

def resize_image(uploaded_file, max_width=800):
    img = Image.open(uploaded_file)

    # アスペクト比を保ったままリサイズ
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    # BytesIOに保存
    buffer = BytesIO()
    img.save(buffer, format=img.format)
    buffer.seek(0)

    return InMemoryUploadedFile(
        buffer, None, uploaded_file.name,
        uploaded_file.content_type, buffer.tell(), None
    )
```

## 使用時の注意

新しいモジュールをインストールしたら、必ず`requirements.txt`に追記してください:

```bash
pip freeze > requirements.txt
```

これにより、他の環境でも同じモジュールをインストールできるようになります。
