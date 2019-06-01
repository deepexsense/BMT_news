from django import forms
from django.contrib import admin

# Register your models here.
from django.core.mail import send_mail

from BMTNews import settings
from BMTNews_App.models import Post, Article, Comment, Section, User, PostComment, News


class NewsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        subscribers = User.objects.filter(is_subscribed=True)
        email_subject = 'Новости БМТ: Уведомление'
        email_body = "На сайте появилась новость под названием \"{}\"".format(obj.news_title)
        send_mail(email_subject, email_body, settings.EMAIL_HOST_USER,
                  [subscribe.email for subscribe in subscribers],
                  fail_silently=False)


admin.site.register(Post)
admin.site.register(Section)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(PostComment)
admin.site.register(News, NewsAdmin)

