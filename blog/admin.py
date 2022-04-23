from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'creation_date')
    list_display_links = ('title', 'slug')
    ordering = ['-creation_date']
    search_fields = ('title', 'slug')
    list_filter = ('creation_date',)
    readonly_fields = ('creation_date',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'level', 'post', 'creation_date', 'parent')
    ordering = ['-creation_date']
    list_filter = ('creation_date',)
    readonly_fields = ('creation_date', 'level')
