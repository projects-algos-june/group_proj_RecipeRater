from django.urls import path
from . import views, validators

urlpatterns = [
    path('', views.index),
    path('register', views.reg_user),
    path('email', validators.email_val),
    path('confpw', validators.pass_val),
    path('login', views.log_user),
    path('email_login', validators.login_email_val),
    path('profile/<int:id>', views.profile),
    path('friend_profile/<int:id>', views.friend_profile),
    path('user_friends/<int:id>', views.user_friends),
    path('add_friend/<int:id>', views.add_friend),
    path('remove_friend/<int:id>', views.remove_friend),
    path('book/<int:id>', views.bookpage),
    path('add_recipe', views.render_add_form),
    path('process_recipe', views.add_recipe),
    path('allrecipes', views.allrecipes),
    path('edit_recipe/<int:id>', views.render_edit_form),
    path('process_recipe_edit/<int:id>', views.process_edit),
    path('delete_recipe/<int:id>', views.delete_recipe),
    path('recipe/<int:id>', views.recipe_page),
    path('recipe/<int:id>/rating', views.rating),
    path('logout', views.logout),
    path('profile_title/<int:id>', views.profile_name_prioity),
    path('profile_book/<int:id>', views.profile_book_priority),
    path('profile_rating/<int:id>', views.profile_rating_priority)
    path('search', views.search),
    path('profile/<int:id>/clear', views.clearsearch),
]
