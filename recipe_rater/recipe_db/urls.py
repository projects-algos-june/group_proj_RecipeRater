from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.reg_user),
    path('login', views.log_user),
    path('profile/<int:id>', views.profile),
    path('add_recipe', views.render_add_form),
    path('process_recipe', views.add_recipe),
    path('edit_recipe/<int:id>', views.render_edit_form),
    path('logout', views.logout),
]
