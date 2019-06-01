from django.conf.urls import url

from BMTNews_App import views

urlpatterns = [
    url(r'^$', views.LastNewsView.as_view(), name='index'),
    url(r'^signup/$', views.SignUpFormView.as_view(), name='signup'),
    url(r'^login/$', views.SignInFormView.as_view(), name='login'),
    url(r'^posts/$', views.PostsView.as_view(), name='posts'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.PostDetailView.as_view(), name='post'),
    url(r'^post/(?P<post_id>[0-9]+)/comment/$', views.add_post_comment, name='add_post_comment'),
    url(r'^forum/$', views.SectionsView.as_view(), name='forum'),
    url(r'^forum/(?P<section>[\w]+)/$', views.ArticleListView.as_view(), name='section'),
    url(r'^forum/(?P<section>[\w]+)/article/(?P<article_id>[0-9]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^forum/article/(?P<article_id>[0-9]+)/comment/$', views.add_comment, name='add_comment'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^contacts/$', views.ContactsView.as_view(), name='contacts'),
    url(r'^user/(?P<id>[0-9]+)/$', views.UserSubscribedView.as_view(), name='user_subscribed'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^feed/$', views.NewsFeed.as_view(), name='feed'),
    url(r'^feed/(?P<news_id>[0-9]+)/$', views.NewsDetailView.as_view(), name='news'),
]
