from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from .models import News
from captcha.fields import CaptchaField


import re


class ContactForm(forms.Form):
    """Форма для отправки обратной связи."""
    subject = forms.CharField(label='тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='содержимое', widget=forms.Textarea(attrs={'class': 'form-control'}))
    captcha = CaptchaField()


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователя."""
    username = forms.CharField(label='имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    """Форма для авторизации пользователя."""
    username = forms.CharField(label='имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class NewsForm(forms.ModelForm):
    """Форма для создения новостей."""
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        # Проверяет начало заголовка.
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('название не должно начинаться с цифры')
        return title

    def clean_content(self):
        # Проверяет текст на запрещенные слова.
        content = self.cleaned_data['content']
        if re.findall(r'дурак|простофиля', content):
            raise ValidationError('запрещено обзываться')
        return content
