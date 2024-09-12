# trade/urls.py
from django.urls import path
from .views import PostListView, PostDetailView  # Убедитесь, что PostDetailView импортирован

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Уберите начальный слеш
]
