from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.reg_user),
    path('login', views.log_user),
    path('success/<int:id>', views.profile),
    path('add_recipe', views.add_recipe),
    path('edit_recipe', views.edit_recipe)
]
