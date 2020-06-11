from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    book = models.ForeignKey(Book, related_name="recipes", on_delete=models.CASCADE)
    rating = models.CharField(max_length=5)
    notes = models.TextField()
    photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    poster = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

