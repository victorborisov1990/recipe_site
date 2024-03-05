from django.contrib import admin

from .models import CategoryModel, RecipeModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    """Список Клиентов"""
    list_display = ['name']
    search_fields = ['name']
    search_help_text = 'Поиск по категориям'

    """Отдельный Клиент"""
    fields = ['name']


@admin.register(RecipeModel)
class RecipeAdmin(admin.ModelAdmin):
    """Список Рецептов"""
    list_display = ['name', 'category', 'author']
    ordering = ['category', 'author']
    search_fields = ['description']
    search_help_text = 'Поиск по описанию'

    """Отдельный рецепт"""
    fieldsets = [
        (
            'Основная информация',
            {
                'classes': ['wide'],
                'fields': ['name', 'category', 'image']
            }
        ),
        (
            'Описание',
            {
                'classes': ['collapse'],
                'fields': ['description', 'steps']
            }
        ),
        (
            'Подробности',
            {
                'fields': ['cook_time', 'author', 'added_date']
            }
        )
    ]
    readonly_fields = ['added_date']
