from django.shortcuts import render, redirect
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def profile(request, id):
    context = {
        'user_info': User.objects.get(id=id)
    }
    return render(request, 'user_profile.html', context)

def reg_user(request):
    if request.method == "POST":
        pw_hash = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['fname'],
            last_name = request.POST['lname'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['user'] = f'{new_user.first_name} {new_user.last_name}'
        request.session['id'] = new_user.id
        request.session['log_status'] = 'registered'
        print("User,", new_user.first_name, new_user.last_name, "has successfully been created")
        return redirect('/success')
    return redirect('/')

def log_user(request):
    if request.method == "POST":
        user_query = User.objects.filter(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['pw'].encode(), user_query.password.encode()):
            request.session['user'] = user_query.first_name + ' ' + user_query.last_name
            request.session['id'] = user_query.id
            request.session['log_status'] = 'logged in'
            print(user_query.first_name, user_query.last_name, "was successfully logged in")
            return redirect('/success')
    return redirect('/')


def add_recipe(request):
    if request.method == "POST":
        new_recipe = recipe.objects.create(
            title = request.POST['title'],
            description = request.POST['desc'],
            book = request.POST['book'],
            rating = None,
            notes = request.POST['notes'],
            photo = None,
            poster = request
        )
        return redirect('/profile')
    return redirect('/')

def edit_recipe(request, id):
    if request.method == "POST":
        return redirect('/')
    return redirect('/')