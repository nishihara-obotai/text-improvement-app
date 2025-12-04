from django.db import models
from django.contrib.auth.models import User


class Text(models.Model):
    """文章改善履歴モデル"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
        related_name="texts"
    )
    original_text = models.TextField(
        verbose_name="元の文章"
    )
    improved_text = models.TextField(
        verbose_name="改善された文章",
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="作成日時"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新日時"
    )
    
    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.username} - {self.original_text[:30]}..."
