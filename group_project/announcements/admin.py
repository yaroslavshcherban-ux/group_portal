from django.contrib import admin
from .models import Announcement, Category, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_at', 'end_date', 'is_pinned']
    list_filter = ['category', 'is_pinned', 'created_at', 'end_date']
    search_fields = ['title', 'content']
    ordering = ['-is_pinned', '-created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
