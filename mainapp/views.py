from django.contrib.auth import logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import RecipeModel
from django.contrib.auth.models import User
from .forms import RecipeForm
from random import choice


def index(request):
    """
    На главной отображаются 5 случайных рецептов
    :param request:
    :return:
    """
    recipes = RecipeModel.objects.all()
    recipe_list = list(recipes)
    recipes_to_main = []
    for _ in range(0, 5):
        if len(recipe_list) > 0:
            recipe = choice(recipe_list)
            recipe_list.remove(recipe)
            recipes_to_main.append(recipe)
    context = {'title': 'Книга рецептов', 'title_h3': 'Добро пожаловать на сайт с рецептами!', 'recipes': recipes_to_main}
    return render(request, 'mainapp/all_recipes.html', context)


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'mainapp/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['title_h3'] = 'Регистрация нового пользователя'
        return context


class Login(LoginView):
    form_class = LoginForm
    template_name = 'mainapp/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['title_h3'] = 'Войдите, чтобы оставлять свои рецепты'
        return context

    def get_success_url(self):
        return reverse_lazy('index')


def logout_me(request):
    logout(request)
    return redirect('login')


def user_recipes(request, user_id):
    get_object_or_404(User, pk=user_id)  # проверка существует ли user. Защита от ручного перехода из адресной строки
    recipes = RecipeModel.objects.filter(author=user_id)
    context = {'title': 'Мои рецепты', 'title_h3': 'Мои рецепты', 'recipes': recipes}
    return render(request, 'mainapp/user_recipes.html', context)


def all_recipes(request):
    recipes = RecipeModel.objects.all()
    context = {'title': 'Все рецепты', 'title_h3': 'Список всех рецептов', 'recipes': recipes}
    return render(request, 'mainapp/all_recipes.html', context)


def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            steps = form.cleaned_data.get('steps')
            cook_time = form.cleaned_data.get('cook_time')
            image = form.cleaned_data.get('image')
            category = form.cleaned_data.get('category')
            author = get_object_or_404(User, pk=request.user.pk)
            RecipeModel.objects.create(
                name=name,
                description=description,
                steps=steps,
                cook_time=cook_time,
                image=image,
                category=category,
                author=author
            )
            return user_recipes(request, request.user.pk)
    else:
        form = RecipeForm()
    context = {
        'form': form,
        'title': 'Новый рецепт',
        'title_h3': 'Добавление нового рецепта'
    }
    return render(request, 'mainapp/new_recipe.html', context)


def get_recipe(request, recipe_id):
    recipe = get_object_or_404(RecipeModel, pk=recipe_id)
    context = {"recipe": recipe, "title": 'Рецепт', 'title_h3': 'Рецепт. Подробный вид'}
    return render(request, 'mainapp/recipe.html', context)


class UpdateRecipe(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = RecipeModel
    fields = ['name', 'description', 'steps', 'cook_time', 'image', 'category']
    success_message = 'Рецепт изменен успешно'
    template_name = 'mainapp/update_recipe.html'
    extra_context = {
        'title': 'Редактирование',
        'title_h3': 'Изменение рецепта'
    }

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.author != self.request.user:
            return render(request, 'mainapp/forbidden.html')
        return super(UpdateRecipe, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('user_recipes', kwargs={'user_id': self.request.user.id})


class DeleteRecipe(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = RecipeModel
    template_name = 'mainapp/delete_recipe.html'
    success_message = 'Рецепт удален успешно'
    extra_context = {
        'title': 'Удаление',
        'title_h3': 'Вы действительно хотите удалить рецепт?'
    }

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('user_recipes', kwargs={'user_id': self.request.user.id})
