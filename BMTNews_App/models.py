from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comments(models.Model):
    path = ArrayField(models.IntegerField())
    post_id = models.ForeignKey(Post, on_delete="CASCADE")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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