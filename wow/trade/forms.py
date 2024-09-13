from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # Используйте CKEditorWidget для RichTextField
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),  # Использовать чекбоксы для выбора категорий
        }
