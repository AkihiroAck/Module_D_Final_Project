from django import forms
from .models import Post, OfferResponse
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # CKEditorWidget для RichTextField
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),  # Чекбоксы для выбора категорий
        }


class OfferResponseForm(forms.ModelForm):
    class Meta:
        model = OfferResponse
        fields = ['content']  # Поле для текста отклика
  