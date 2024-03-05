from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import CategoryModel, RecipeModel
# from django.utils.translation import ugettext_lazy as _


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RecipeForm(forms.ModelForm):
    name = forms.CharField(label='Название рецепта', widget=forms.TextInput(attrs={'class': 'form-input'}))
    description = forms.CharField(label='Описание блюда', widget=forms.Textarea(attrs={'class': 'form-input'}))
    steps = forms.CharField(label='Шаги приготовления, разделенные ";"', widget=forms.Textarea(attrs={'class': 'form-input'}))
    cook_time = forms.CharField(label='Время приготовления', widget=forms.TextInput(attrs={'class': 'form-input'}))
    image = forms.ImageField(label='Изображение', required=False)

    class Meta:
        model = RecipeModel
        fields = ('name',
                  'description',
                  'steps',
                  'cook_time',
                  'image',
                  'category')
        labels = {
            'category': 'Категория',
        }
