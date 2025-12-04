# Userモデルの拡張

ユーザー情報を拡張する必要がある場合、**AbstractUserを継承するのではなく、UserProfileモデルを作成する方法を推奨**します。これは初級者にとって理解しやすく、既存のDjango認証システムに影響を与えにくいためです。

## 推奨方法: UserProfileモデルを使う

### 1. モデルの作成

```python
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='電話番号')
    department = models.CharField(max_length=100, blank=True, verbose_name='部署')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='アバター')
    bio = models.TextField(blank=True, verbose_name='自己紹介')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    class Meta:
        verbose_name = 'ユーザープロフィール'
        verbose_name_plural = 'ユーザープロフィール'

    def __str__(self):
        return f"{self.user.username}のプロフィール"
```

### 2. Adminの設定

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# UserProfileをインライン表示
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'プロフィール'

# 既存のUserAdminを拡張
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# 既存のUserAdminを解除して、新しいUserAdminを登録
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
```

### 3. Signalで自動作成（オプション）

新規ユーザー作成時に自動的にUserProfileを作成する場合：

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

`apps.py`でSignalを有効化：

```python
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals  # Signalをインポート
```

### 4. ビューでの使用

```python
from django.shortcuts import render
from .models import UserProfile

def profile_view(request):
    # get_or_createで確実にProfileを取得
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'profile.html', {'profile': profile})

def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number', '')
        profile.department = request.POST.get('department', '')
        profile.bio = request.POST.get('bio', '')
        profile.save()

        return redirect('profile')

    return render(request, 'profile_edit.html', {'profile': profile})
```

### 5. テンプレートでの使用

```django
<!-- プロフィール表示 -->
<div class="profile">
    <h2>{{ request.user.username }}</h2>
    <p>メールアドレス: {{ request.user.email }}</p>
    <p>電話番号: {{ request.user.profile.phone_number }}</p>
    <p>部署: {{ request.user.profile.department }}</p>
    <p>自己紹介: {{ request.user.profile.bio }}</p>

    {% if request.user.profile.avatar %}
        <img src="{{ request.user.profile.avatar.url }}" alt="アバター">
    {% endif %}
</div>
```

### 6. フォームでの使用

```python
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'department', 'bio', 'avatar']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'department': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'bio': forms.Textarea(attrs={'class': 'textarea textarea-bordered', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'file-input file-input-bordered'}),
        }

# ビューでの使用
def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})
```

## メリット

- **シンプル**: 既存のUser認証システムをそのまま利用
- **安全**: Django標準の認証機能に影響を与えない
- **理解しやすい**: 初級者でも理解・実装が容易
- **柔軟**: 後から簡単にフィールドを追加・削除可能
- **マイグレーションが簡単**: プロジェクト途中でも追加可能

## 非推奨: AbstractUserの継承

AbstractUserやAbstractBaseUserを継承する方法は、以下の理由で推奨しません：

### デメリット

1. **プロジェクト開始時からの設計が必要**
   - 既存プロジェクトに後から追加するのが困難
   - マイグレーションが複雑になる

2. **初級者には理解が難しい**
   - AUTH_USER_MODELの設定が必要
   - 既存の認証システムとの統合が複雑

3. **リスクが高い**
   - 設定ミスで認証システム全体が動作しなくなる可能性
   - ロールバックが困難

### 使用すべき場合

以下の場合のみ、AbstractUserの継承を検討してください：

- **プロジェクト開始時から設計**している場合
- **メールアドレスでログイン**など、認証方式自体を変更する場合
- **チームに経験者**がいる場合

## まとめ

ほとんどのケースでは、**UserProfileモデルを使う方法で十分**です。シンプルで安全、そして柔軟性が高いため、初級者から上級者まで幅広く使えます。
