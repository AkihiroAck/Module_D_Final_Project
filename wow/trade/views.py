from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = self.get_object()

        context['user_is_author'] = user.is_authenticated and user == post.author
        context['user_is_staff'] = user.is_authenticated and user.is_staff
        return context


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
        return self.request.user.is_superuser or post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')  # Перенаправление на список постов после удаления

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_superuser or post.author == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return super().handle_no_permission()
        return super().handle_no_permission()
    

# Перенаправление на страницу входа
class SignupRedirectView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('account_login'))
        