# trade/urls.py
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, DeleteAccountView, SignupRedirectView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('accounts/signup/', SignupRedirectView.as_view(), name='signup_redirect'),
]
