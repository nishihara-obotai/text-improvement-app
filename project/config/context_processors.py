from django.conf import settings


def site_settings(request):
    """
    サイト設定を全テンプレートで利用可能にするcontext processor
    settings.pyのSITE_NAMEを{{ SITE_NAME }}で参照できるようになります
    """
    return {
        "SITE_NAME": settings.SITE_NAME,
    }
