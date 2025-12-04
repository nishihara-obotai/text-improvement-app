#!/usr/bin/env python
"""
render.comデプロイ時にユーザーを作成するスクリプト
"""

import os

import django
from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def create_users():
    """デプロイ時にユーザーを作成"""

    # スーパーユーザーの作成
    if not User.objects.filter(username="obot-ai-admin").exists():
        User.objects.create_superuser(
            username="obot-ai-admin", email="admin@example.com", password="admin-qwer"
        )
        print("✓ スーパーユーザー obot-ai-admin を作成しました")
    else:
        print("- スーパーユーザー obot-ai-admin は既に存在します")

    # 一般ユーザーの作成
    if not User.objects.filter(username="obot-ai-user").exists():
        User.objects.create_user(
            username="obot-ai-user", email="user@example.com", password="user-qwer"
        )
        print("✓ ユーザー obot-ai-user を作成しました")
    else:
        print("- ユーザー obot-ai-user は既に存在します")


if __name__ == "__main__":
    create_users()
