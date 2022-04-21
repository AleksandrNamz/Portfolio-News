from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


from news.models import News, Category
from .forms import *
from .utils import MyMixin


def contact(request):
    # Вызывает форму для обратной связи.
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'zapolni@mail.svoy',
                             ['zapolni@mail.adresata'], fail_silently=True)
            if mail:
                messages.success(request, 'письмо успешно отправлено :)')
                return redirect('contact')
            else:
                messages.error(request, 'что-то пошло не так :(')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', {'form': form})


def register(request):
    # Вызывает форму для регистрации пользователя.
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ваша учетная запись успешно создана! :)')
            return redirect('home')
        else:
            messages.error(request, 'что-то пошло не так :(')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    # Вызывает форму для авторизации.
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


class HomeNews(MyMixin, ListView):
    """Основной класс для отображения новостей."""
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    # Добавить в родительский словарь необходимый контекст.
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_lower('Главная страница')
        return context

    # Представить только новости для публикации.
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    """Выводит новости по категориям."""
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    # title == текущая выбранная категория.
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_lower(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    # Представит новости по категориям, только опубликованные
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    """Класс для представления одной новости."""
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'


class AddNews(LoginRequiredMixin, CreateView):
    """Класс для добавления новости."""
    form_class = NewsForm
    template_name = 'news/add_news.html'
    raise_exception = True

