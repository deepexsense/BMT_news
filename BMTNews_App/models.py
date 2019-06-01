from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class User(AbstractUser):
    is_subscribed = models.BooleanField(default=False)


class Section(models.Model):
    section_title = models.CharField(max_length=200)
    section_url = models.CharField(max_length=50)
    section_description = models.TextField()

    def __str__(self):
        return self.section_title


class Article(models.Model):
    article_title = models.CharField(max_length=200)
    article_section = models.ForeignKey(Section, on_delete=models.CASCADE)
    article_author = models.ForeignKey(User, on_delete=models.CASCADE)
    article_date = models.DateTimeField(default=timezone.now)
    article_content = models.TextField()
    article_status = models.IntegerField()

    def __str__(self):
        return self.article_title

    def get_absolute_url(self):
        return reverse('article', kwargs={'section': self.article_section.section_url,
                                          'article_id': self.id})


class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    post_created_date = models.DateTimeField(default=timezone.now)
    post_published_date = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.id})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.post_title


class PostComment(models.Model):
    path = ArrayField(models.IntegerField(default=None))
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content[0:200]

    def get_offset(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return level

    def get_col(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return 12 - level


class Comment(models.Model):
    path = ArrayField(models.IntegerField(default=None))
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, default=1)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content[0:200]

    def get_offset(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return level

    def get_col(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return 12 - level


class News(models.Model):
    news_title = models.CharField(max_length=100)
    news_text = models.TextField()
    news_img = models.ImageField(upload_to='')
    news_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.news_text[0:20]