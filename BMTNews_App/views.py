from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView, ListView, DetailView
from django.views.generic.base import View

from BMTNews_App.forms import SignUpForm, CommentForm
from BMTNews_App.models import Post


class SignUpFormView(FormView):
    form_class = SignUpForm
    template_name = 'BMTNews_App/registration/register.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(SignUpFormView, self).form_valid(form)


class SignInFormView(FormView):
    form_class = AuthenticationForm
    success_url = '/'

    template_name = 'BMTNews_App/registration/login.html'

    def form_valid(self, form):
        user = authenticate(**form.cleaned_data)
        if user:
            login(self.request, user)
        return super(SignInFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'BMTNews_App/index.html', {})


class PostsView(ListView):
    model = Post
    template_name = 'BMTNews_App/posts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context


class PostDetailView(DetailView):
    template_name = 'BMTNews_App/detail.html'

    def get_object(self, queryset=None):
        post = Post.objects.get(id=self.kwargs['id'])
        return post
