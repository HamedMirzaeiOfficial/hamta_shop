from django.contrib import admin
from .models import Post, Comment
from tinymce.widgets import TinyMCE
from django.db import models
from .forms import FlatPageForm




class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    add_form = FlatPageForm()
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    inlines = [CommentInline, ]

admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'post', 'created', 'active', 'user']
    list_filter = ['active', 'created', 'post', 'user']
    search_fields = ['title', 'email', 'body']

