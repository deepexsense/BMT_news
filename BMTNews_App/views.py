from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.syndication.views import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView, ListView, DetailView
from django.views.generic.base import View

from BMTNews import settings
from BMTNews_App.forms import SignUpForm, CommentForm, ContactForm
from BMTNews_App.models import Post, Section, Article, Comment, PostComment, User, News


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
        return render(request, 'BMTNews_App/registration/logout.html', {})


class PostsView(ListView):
    model = Post
    template_name = 'BMTNews_App/blog/posts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    comment_form = CommentForm
    template_name = 'BMTNews_App/blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {'post': get_object_or_404(Post, id=self.kwargs['post_id'])}
        context.update(csrf(self.request))
        user = auth.get_user(self.request)
        context['comments'] = context['post'].postcomment_set.all().order_by('path')
        context['next'] = context['post'].get_absolute_url()
        if user.is_authenticated:
            context['form'] = self.comment_form
        return context


class SearchView(ListView):
    model = Post
    template_name = 'BMTNews_App/blog/search.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = {}

        question = self.request.GET.get('q')
        if question is not None:
            search_posts = Post.objects.filter(post_content__icontains=question)
            context['last_question'] = '?q=%s' % question
            current_page = Paginator(search_posts, 10)
            page = self.request.GET.get('page')
            try:
                context['posts'] = current_page.page(page)
            except PageNotAnInteger:
                context['posts'] = current_page.page(1)
            except EmptyPage:
                context['posts'] = current_page.page(current_page.num_pages)
        return context


@login_required
@require_http_methods(["POST"])
def add_post_comment(request, post_id):
    form = CommentForm(request.POST)
    post = get_object_or_404(Post, id=post_id)

    if form.is_valid():
        comment = PostComment()
        comment.path = []
        comment.post_id = post
        comment.user_id = auth.get_user(request)
        comment.content = form.cleaned_data['comment_area']
        comment.save()
        try:
            comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
            comment.path.append(comment.id)
        except ObjectDoesNotExist:
            comment.path.append(comment.id)

        comment.save()

    return redirect(post.get_absolute_url())


class SectionsView(ListView):
    model = Section
    template_name = 'BMTNews_App/forum/forum.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        all_sections = Section.objects.all().order_by('section_title')
        current_page = Paginator(all_sections, 10)
        page = self.request.GET.get('page')
        try:
            context['section_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['section_list'] = current_page.page(1)
        except EmptyPage:
            context['section_list'] = current_page.page(current_page.num_pages)
        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'BMTNews_App/forum/section.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {'section': get_object_or_404(Section, section_url=self.kwargs['section'])}
        all_articles = Article.objects.filter(article_status=True).order_by('-article_date')
        current_page = Paginator(all_articles, 10)
        page = self.request.GET.get('page')
        try:
            context['article_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['article_list'] = current_page.page(1)
        except EmptyPage:
            context['article_list'] = current_page.page(current_page.num_pages)
        return context


class ArticleView(DetailView):
    model = Article
    comment_form = CommentForm
    template_name = 'BMTNews_App/forum/article.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Article, pk=self.kwargs['article_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {'article': get_object_or_404(Article, id=self.kwargs['article_id'])}
        context.update(csrf(self.request))
        user = auth.get_user(self.request)
        context['comments'] = context['article'].comment_set.all().order_by('path')
        context['next'] = context['article'].get_absolute_url()
        if user.is_authenticated:
            context['form'] = self.comment_form
        return context


@login_required
@require_http_methods(["POST"])
def add_comment(request, article_id):
    form = CommentForm(request.POST)
    article = get_object_or_404(Article, id=article_id)

    if form.is_valid():
        comment = Comment()
        comment.path = []
        comment.article_id = article
        comment.user_id = auth.get_user(request)
        comment.content = form.cleaned_data['comment_area']
        comment.save()
        try:
            comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
            comment.path.append(comment.id)
        except ObjectDoesNotExist:
            comment.path.append(comment.id)

        comment.save()

    return redirect(article.get_absolute_url())


class ContactsView(FormView):
    template_name = 'BMTNews_App/contact/contact_form.html'
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        email_subject = 'Новости БМТ: Сообщение через контактную форму'
        email_body = "С сайта отправлено новое сообщение\n\n" \
                     "Имя отправителя: %s \n" \
                     "E-mail отправителя: %s \n\n" \
                     "Сообщение: \n" \
                     "%s " % \
                     (form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message'])
        send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER],
                  fail_silently=False)
        return super(ContactsView, self).form_valid(form)


@method_decorator(csrf_exempt, 'dispatch')
class UserSubscribedView(View):

    def post(self, request, id):
        user = User.objects.get(id=self.kwargs["id"])
        user.is_subscribed = not user.is_subscribed
        user.save()
        return HttpResponse()


class NewsFeed(ListView):
    model = News
    template_name = 'BMTNews_App/feed.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        all_news = News.objects.all().order_by('-news_date')
        current_page = Paginator(all_news, 4)
        page = self.request.GET.get('page')
        try:
            context['news_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['news_list'] = current_page.page(1)
        except EmptyPage:
            context['news_list'] = current_page.page(current_page.num_pages)
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'BMTNews_App/piece_of_news.html'

    def get_object(self, queryset=None):
        return get_object_or_404(News, pk=self.kwargs['news_id'])


class LastNewsView(ListView):
    model = News
    template_name = 'BMTNews_App/index.html'

    def get_context_data(self, **kwargs):
        context = {'last_news': News.objects.last()}
        last_news_list = News.objects.all().order_by('-news_date')[:4]
        context['last_news_list'] = last_news_list
        return context
