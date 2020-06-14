from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def profile(request, id):
    user_info = User.objects.get(id=id)
    context = {
        'user_recipes': user_info.posted_recipes.all()
    }
    return render(request, 'user_profile.html', context)

def render_add_form(request):
    return render(request, 'add_recipe.html')

def render_edit_form(request, id):
    context = {
        'curr_recipe': Recipe.objects.get(id=id)
    }
    return render(request, 'edit_recipe.html', context)

def reg_user(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        else:
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
            return redirect('/profile/'+str(new_user.id))
    return redirect('/')

def log_user(request):
    if request.method == "POST":
        user_query = User.objects.filter(email=request.POST['email'])
        if len(user_query) > 0:
            user_query = user_query[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), user_query.password.encode()):
                request.session['user'] = user_query.first_name + ' ' + user_query.last_name
                request.session['id'] = user_query.id
                request.session['log_status'] = 'logged in'
                print(user_query.first_name, user_query.last_name, "was successfully logged in")
                return redirect('/profile/'+str(user_query.id))
    return redirect('/')

def logout(request):
    if request.method == "POST":
        print(request.session['user'], "has been successfully logged out")
        request.session.flush()
        print("Session has been flushed")
        return redirect('/')
    return redirect('/profile'+str(request.session['id']))


def add_recipe(request):
    if request.method == "POST":
        # Filter for existing cookbooks
        book_query = Book.objects.filter(title=request.POST['book'])
        if len(book_query) > 0:
            # Add new photo to file system
            pic = request.FILES['photo']
            fs = FileSystemStorage()
            new_photo = fs.save(pic.name, pic)
            url = fs.url(new_photo)

            # Change querySet to single item
            book_query = book_query[0]
            # Create new recipe
            new_recipe = Recipe.objects.create(
                title = request.POST['title'],
                description = request.POST['desc'],
                book = book_query,
                rating = None,
                notes = request.POST['notes'],
                photo = url,
                poster = User.objects.get(id=request.session['id'])
            )
            print(f'{new_recipe.title} recipe successfully created for {new_recipe.book.title}')
        else:
            # Add new photo to file system
            pic = request.FILES['photo']
            fs = FileSystemStorage()
            new_photo = fs.save(pic.name, pic)
            url = fs.url(new_photo)

            # If cookbook not found, create new cookbook from title
            new_book = Book.objects.create(title=request.POST['book'])
            # Create new recipe
            new_recipe = Recipe.objects.create(
                title = request.POST['title'],
                description = request.POST['desc'],
                book = new_book,
                rating = None,
                notes = request.POST['notes'],
                photo = url,
                poster = User.objects.get(id=request.session['id'])
            )
            print(f'{new_recipe.title} recipe successfully created for {new_recipe.book.title}')
            
        
        
        return redirect('/profile/'+str(request.session['id']))
    return redirect('/')

def edit_recipe(request, id):
    if request.method == "POST":
        
        return redirect('/')
    return redirect('/')

# def delete_recipe(request, id):
#     if request.method == "POST":
#         to_delete = Recipe.objects.get(id=id)
#         to_delete.delete()
#         return redirect('/profile')




