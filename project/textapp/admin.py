from django.contrib import admin
from .models import Text


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ["user", "original_text_preview", "created_at", "updated_at"]
    list_filter = ["created_at", "user"]
    search_fields = ["original_text", "improved_text"]
    readonly_fields = ["created_at", "updated_at"]
    
    def original_text_preview(self, obj):
        return obj.original_text[:50] + "..." if len(obj.original_text) > 50 else obj.original_text
    
    original_text_preview.short_description = "元の文章"
