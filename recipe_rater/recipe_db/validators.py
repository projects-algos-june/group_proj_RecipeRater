from django.shortcuts import render, redirect
from django.conf import settings
from .models import *


"""
Ajax Validations for Register and Login Page
"""

"""
Validation for register email
"""
def email_val(request):
    if request.method == "POST":
        found = False
        user_query = User.objects.filter(email=request.POST['email'])
        print(user_query)
        if len(user_query) > 0:
            found = True
        context = {
            'found': found
        }
        return render(request, 'partials/email.html', context)    
    return redirect('/')

"""
Validation for login email
"""
def login_email_val(request):
    if request.method == "POST":
        found = False
        user_query = User.objects.filter(email=request.POST['email'])
        print(user_query)
        if len(user_query) > 0:
            found = True
        context = {
            'found': found
        }
        return render(request, 'partials/login_email.html', context)    
    return redirect('/')

"""
If pass and confirm pass are equal -- validation in .js
"""
def pass_val(request):
    if request.method == "POST":
        confirmed = True
        context = {
            'confirm': confirmed
        }
        return render(request, 'partials/confirm.html', context)
    return redirect('/')