from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post, OfferResponse
from .forms import PostForm, OfferResponseForm

# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Присваиваем текущего пользователя как автора
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_detail')

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        return user.is_superuser or post.author == user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            return redirect('account_login')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        return user.is_superuser or post.author == user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            return redirect('account_login')


class OfferResponseView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = OfferResponse
    template_name = 'offer_response_detail.html'
    context_object_name = 'response'
    
    def test_func(self):
        response = self.get_object()
        user = self.request.user
        return response.client == user or response.post.author == user or user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            return redirect('account_login')


class OfferResponseAcceptView(LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        response = get_object_or_404(OfferResponse, pk=kwargs['pk'])
        
        # Проверяем, что пользователь - автор поста
        if request.user == response.post.author:
            response.is_accepted = True
            response.save()
        
        return redirect('offer_response_detail', pk=response.pk)
        
    
class AuthorPostResponsesView(LoginRequiredMixin, ListView):
    model = OfferResponse
    template_name = 'offer_response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        # Получаем все отклики на посты текущего пользователя и сортируем по дате создания (новые сверху)
        return OfferResponse.objects.filter(post__author=self.request.user).select_related('post').order_by('-created_at')
        
    
class UserPostResponsesView(LoginRequiredMixin, ListView):
    model = OfferResponse
    template_name = 'offer_response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        # Получаем все отклики на посты текущего пользователя и сортируем по дате создания (новые сверху)
        return OfferResponse.objects.filter(client=self.request.user).select_related('post').order_by('-created_at')


class OfferResponseCreateView(LoginRequiredMixin, CreateView):
    model = OfferResponse
    form_class = OfferResponseForm
    template_name = 'offer_response_create.html'

    def form_valid(self, form):
        # Привязываем отклик к текущему пользователю
        form.instance.client = self.request.user
        # Привязываем отклик к посту
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class OfferResponseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OfferResponse
    template_name = 'offer_response_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        response = self.get_object()
        user = self.request.user
        return user.is_superuser or response.post.author == user or response.client == user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            return redirect('account_login')


# Перенаправление на страницу входа
class SignupRedirectView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('account_login'))


class DeleteAccountView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User  # Используйте модель User
    template_name = 'delete_account.html'
    success_url = reverse_lazy('post_list')  # Перенаправление после успешного удаления

    def get_object(self, queryset=None):
        return self.request.user  # Удаление текущего пользователя

    def test_func(self):
        # Проверка, что пользователь удаляет только свой аккаунт
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            return redirect('account_login')
