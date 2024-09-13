import os
from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.files.storage import default_storage

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Автор поста
    categories = models.ManyToManyField(Category)  # Множественные категории
    title = models.CharField(max_length=200)
    content = RichTextField()  # WYSIWYG редактор для текстового контента
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Поле для изображения
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)  # Поле для видео
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Проверяем, есть ли старое изображение
        if self.pk:
            old_post = Post.objects.get(pk=self.pk)
            if old_post.image and old_post.image != self.image:
                # Удаляем старое изображение, если оно было заменено
                if default_storage.exists(old_post.image.path):
                    default_storage.delete(old_post.image.path)
            if old_post.video and old_post.video != self.video:
                # Удаляем старое видео, если оно было заменено
                if default_storage.exists(old_post.video.path):
                    default_storage.delete(old_post.video.path)
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        # Удаляем связанные файлы при удалении объекта
        if self.image and default_storage.exists(self.image.path):
            default_storage.delete(self.image.path)
        if self.video and default_storage.exists(self.video.path):
            default_storage.delete(self.video.path)

        # Вызываем метод delete родительского класса
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


# Отклик
class OfferResponse(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Автор отклика
    post = models.ForeignKey(Post, related_name='responses', on_delete=models.CASCADE)  # Пост, к которому привязан отклик
    content = models.TextField()  # Содержимое отклика
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f'{self.author} откликнулся на {self.post.title}:{self.content}'
