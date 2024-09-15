from django import forms
from .models import Post, OfferResponse, Category
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # CKEditorWidget для RichTextField
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),  # Чекбоксы для выбора категорий
        }

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Bootstrap класс для стилизации
            'placeholder': 'Введите заголовок поста'  # Подсказка для пользователя
        }),
        label='Заголовок',  # Подпись для поля
    )

    content = forms.CharField(
        widget=CKEditorWidget(attrs={
            'class': 'form-control',  # Bootstrap класс для стилизации
        }),  # CKEditorWidget для RichTextField
        label='Содержание',  # Подпись для поля
    )
    
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',  # Bootstrap класс для загрузки файлов
        }),
        label='Изображение',  # Подпись для поля
        required=False,  # Поле необязательное
    )
    
    video = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',  # Bootstrap класс для загрузки файлов
        }),
        label='Видео',  # Подпись для поля
        required=False,  # Поле необязательное
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # Список всех доступных категорий
        widget=forms.CheckboxSelectMultiple(),
        label='Категории',  # Подпись для поля
    )


class OfferResponseForm(forms.ModelForm):
    class Meta:
        model = OfferResponse
        fields = ['content']  # Поле для текста отклика

    # Настройка виджетов для более красивого представления формы
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',  # Bootstrap класс для стилизации
            'rows': 5,  # Количество строк для текстового поля
            'placeholder': 'Введите ваш отклик здесь...'  # Подсказка
        }),
        label='',  # Подпись к полю
    )
  