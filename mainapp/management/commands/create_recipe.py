from django.core.management.base import BaseCommand
from mainapp.models import RecipeModel, CategoryModel
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.get(username='user1')
        category = CategoryModel.objects.get(name='Напитки')
        recipe = RecipeModel.objects.create(
                                            name='Чай',
                                            description='Бодрящий напиток',
                                            steps='Положить пакетик, залить горячей водой',
                                            cook_time='2 минуты',
                                            author=user,
                                            category=category
                                            )
        print(f'Создан рецепт: {recipe}')
