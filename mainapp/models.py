from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class CategoryModel(models.Model):
    """
    Поля модели «Категория»:
    — название категории
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class RecipeModel(models.Model):
    """
    ○ Название
    ○ Описание
    ○ Шаги приготовления
    ○ Время приготовления
    ○ Изображение
    ○ Автор
    ○ *другие поля на ваш выбор, например ингредиенты и т.п.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    steps = models.TextField()
    cook_time = models.CharField(max_length=15)
    image = models.ImageField(upload_to='recipes', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('get_recipe', kwargs={'recipe_id': self.pk})

    def split_steps(self):
        return self.steps.split(';')
