from django.conf.urls import url

from BMTNews_App import views

urlpatterns = [
    url(r'^$', views.TemplateView.as_view(template_name='BMTNews_App/index.html'), name='index'),
    url(r'^signup/$', views.SignUpFormView.as_view(), name='signup'),
    url(r'^login/$', views.SignInFormView.as_view(), name='login'),
    url(r'^posts/$', views.PostsView.as_view(), name='posts'),
    url(r'^post/(?P<id>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    # url(r'^post/comment/(?P<id>[0-9]+)/$', views.add_comment, name='add_comment'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
