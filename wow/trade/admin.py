from django.contrib import admin
from .models import Category, Post

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Поля, которые будут отображаться в списке категорий
    search_fields = ('title',)  # Поля, по которым будет производиться поиск


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    