from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_me, name='logout'),
    path('new_recipe/', views.new_recipe, name='new_recipe'),
    path('user_recipes/<int:user_id>/', views.user_recipes, name='user_recipes'),
    path('all_recipes/', views.all_recipes, name='all_recipes'),
    path('recipe/<int:recipe_id>/', views.get_recipe, name='get_recipe'),
    path('update_recipe/<int:pk>/', views.UpdateRecipe.as_view(), name='update_recipe'),
    path('delete_recipe/<int:pk>/', views.DeleteRecipe.as_view(), name='delete_recipe'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
