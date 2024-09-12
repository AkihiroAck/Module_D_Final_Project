from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

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
    video_url = models.URLField(blank=True, null=True)  # Поле для ссылки на видео
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Отклик
class OfferResponse(models.Model):
    pass
