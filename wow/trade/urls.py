# trade/urls.py
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, DeleteAccountView, SignupRedirectView, OfferResponseDeleteView, AuthorPostResponsesView, OfferResponseView, OfferResponseAcceptView, OfferResponseCreateView, UserPostResponsesView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('offer-response/<int:pk>/', OfferResponseView.as_view(), name='offer_response_detail'),
    path('offer-response/<int:pk>/delete/', OfferResponseDeleteView.as_view(), name='offer_response_delete'),
    path('offer-response/<int:pk>/accept', OfferResponseAcceptView.as_view(), name='offer_response_accept'),
    path('author-responses/', AuthorPostResponsesView.as_view(), name='author_responses'),
    path('user-responses/', UserPostResponsesView.as_view(), name='user_responses'),
    path('post/<int:pk>/offer-response-create/', OfferResponseCreateView.as_view(), name='offer_response_create'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    # path('accounts/signup/', SignupRedirectView.as_view(), name='signup_redirect'),
]
