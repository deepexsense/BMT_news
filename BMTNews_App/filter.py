import django_filters
from django.forms import TextInput
from BMTNews_App.models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains',
                                      widget=TextInput(attrs={'placeholder': 'Title'}))

    class Meta:
        model = Post
        fields = ["title",]
