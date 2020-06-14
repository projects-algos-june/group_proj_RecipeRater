from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address")
        if len(postData['fname']) < 2:
            errors['first_name'] = ("First name must be at least 2 characters")
        if len(postData['lname']) < 2:
            errors['last_name'] = ("Last name must be at least 2 characters")
        if len(postData['pw']) < 8:
            errors['password'] = ("Password must be at least 8 characters")
        if postData['pw'] != postData['confpw']:
            errors['conf_pass'] = ("Password and Confirm Password must match")
        return errors
    
    def edit_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address")
        if len(postData['fname']) < 2:
            errors['first_name'] = ("First name must be at least 2 characters")
        if len(postData['lname']) < 2:
            errors['last_name'] = ("Last name must be at least 2 characters")
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    book = models.ForeignKey(Book, related_name="recipes", on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, null=True)
    notes = models.TextField()
    photo = models.FileField(upload_to="images", null=True)
    poster = models.ForeignKey(User, related_name="posted_recipes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

