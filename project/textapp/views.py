from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Text
from .utils import improve_text


@require_http_methods(["GET", "POST"])
def login_view(request):
    """ログインビュー"""
    if request.user.is_authenticated:
        return redirect("textapp:home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "ログインしました")
            return redirect("textapp:home")
        else:
            messages.error(request, "ユーザー名またはパスワードが正しくありません")

    return render(request, "textapp/login.html")


def logout_view(request):
    """ログアウトビュー"""
    logout(request)
    messages.success(request, "ログアウトしました")
    return redirect("textapp:login")


@login_required
@require_http_methods(["GET", "POST"])
def home_view(request):
    """ホームページ（文章入力・改善）"""
    improved_text = None
    original_text = ""

    if request.method == "POST":
        action = request.POST.get("action")
        original_text = request.POST.get("original_text", "").strip()

        if not original_text:
            messages.error(request, "文章を入力してください")
        elif action == "improve":
            # 文章を改善
            try:
                improved_text = improve_text(original_text)
            except Exception as e:
                messages.error(request, str(e))
        elif action == "save":
            # 履歴に保存
            improved_text = request.POST.get("improved_text", "")
            if improved_text:
                Text.objects.create(
                    user=request.user,
                    original_text=original_text,
                    improved_text=improved_text,
                )
                messages.success(request, "履歴に保存しました")
                return redirect("textapp:history_list")
            else:
                messages.error(request, "改善された文章がありません")

    return render(
        request,
        "textapp/home.html",
        {
            "original_text": original_text,
            "improved_text": improved_text,
        },
    )


@login_required
def history_list_view(request):
    """履歴一覧ページ"""
    texts = Text.objects.filter(user=request.user)
    return render(
        request,
        "textapp/history_list.html",
        {
            "texts": texts,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def history_detail_view(request, pk):
    """履歴詳細・編集ページ"""
    text = get_object_or_404(Text, pk=pk, user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "improve":
            # 再改善
            original_text = request.POST.get("original_text", "").strip()
            if original_text:
                try:
                    improved_text = improve_text(original_text)
                    text.original_text = original_text
                    text.improved_text = improved_text
                    text.save()
                    messages.success(request, "文章を再改善しました")
                except Exception as e:
                    messages.error(request, str(e))
            else:
                messages.error(request, "文章を入力してください")
        elif action == "save":
            # 保存
            original_text = request.POST.get("original_text", "").strip()
            improved_text = request.POST.get("improved_text", "").strip()
            if original_text and improved_text:
                text.original_text = original_text
                text.improved_text = improved_text
                text.save()
                messages.success(request, "保存しました")
            else:
                messages.error(request, "文章を入力してください")

    return render(
        request,
        "textapp/history_detail.html",
        {
            "text": text,
        },
    )


@login_required
@require_http_methods(["POST"])
def history_delete_view(request, pk):
    """履歴削除"""
    text = get_object_or_404(Text, pk=pk, user=request.user)
    text.delete()
    messages.success(request, "履歴を削除しました")
    return redirect("textapp:history_list")
