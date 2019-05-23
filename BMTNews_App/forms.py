from django import forms
from django.contrib.auth.forms import UserCreationForm

from BMTNews_App.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label='Имя пользователя')
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')
    email = forms.EmailField(max_length=100, required=True)
    password2 = forms.CharField(required=True, label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class CommentForm(forms.Form):
    parent_comment = forms.IntegerField(widget=forms.HiddenInput, required=False)
    comment_area = forms.CharField(label="", widget=forms.Textarea)


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    message = forms.CharField(label="Сообщение",widget=forms.Textarea)
