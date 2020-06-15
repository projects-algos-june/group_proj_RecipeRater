from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import *
import bcrypt


#### Page Renders for site
# Log/Register page
def index(request):
    return render(request, 'index.html')

# Renders recipes added by user
def profile(request, id):
    user_info = User.objects.get(id=id)
    context = {
        'user_recipes': user_info.posted_recipes.all()
    }
    for recipe in context['user_recipes']:
        print(recipe.title)
    return render(request, 'user_profile.html', context)

# Renders form to create new recipe
def render_add_form(request):
    return render(request, 'add_recipe.html')

# Renders form to edit existing recipe
def render_edit_form(request, id):
    context = {
        'curr_recipe': Recipe.objects.get(id=id)
    }
    return render(request, 'edit_recipe.html', context)

# Renders page displaying recipe
def recipe_page(request, id):
    context = {
        'curr_recipe': Recipe.objects.get(id=id)
    }
    return render(request, 'recipe_page.html', context)



#### Redirect functionality of website
# Register user
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

# Log user and add to request.session
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

# Flush user from request.session and return to Login page
def logout(request):
    if request.method == "POST":
        print(request.session['user'], "has been successfully logged out")
        request.session.flush()
        print("Session has been flushed")
        return redirect('/')
    return redirect('/profile'+str(request.session['id']))

# Process form for adding recipe
def add_recipe(request):
    if request.method == "POST" and request.FILES.get('photo', False):
        # Add new photo to file system if present
        pic = request.FILES['photo']
        fs = FileSystemStorage()
        new_photo = fs.save(pic.name, pic)
        url = fs.url(new_photo)

        # Filter for existing cookbooks
        book_query = Book.objects.filter(title=request.POST['book'])
        if len(book_query) > 0:
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
    elif request.method == "POST":
        # Filter for existing cookbooks
        book_query = Book.objects.filter(title=request.POST['book'])
        if len(book_query) > 0:
            # Change querySet to single item
            book_query = book_query[0]
            # Create new recipe
            new_recipe = Recipe.objects.create(
                title = request.POST['title'],
                description = request.POST['desc'],
                book = book_query,
                rating = None,
                notes = request.POST['notes'],
                photo = None,
                poster = User.objects.get(id=request.session['id'])
            )
            print(f'{new_recipe.title} recipe successfully created for {new_recipe.book.title}')
        else:
            # If cookbook not found, create new cookbook from title
            new_book = Book.objects.create(title=request.POST['book'])
            # Create new recipe
            new_recipe = Recipe.objects.create(
                title = request.POST['title'],
                description = request.POST['desc'],
                book = new_book,
                rating = None,
                notes = request.POST['notes'],
                photo = None,
                poster = User.objects.get(id=request.session['id'])
            )
            print(f'{new_recipe.title} recipe successfully created for {new_recipe.book.title}')
        return redirect('/profile/'+str(request.session['id']))
    return redirect('/profile/'+str(request.session['id']))


# Process form for editing existing recipe
def process_edit(request, id):
    if request.method == "POST":
        # With file upload
        # retrieve working recipe and cookbook
        to_edit = Recipe.objects.get(id=id)
        book_query = Book.objects.filter(title=request.POST['book'])
        if len(book_query) > 0:
            book_query = book_query[0]
        else:
            # If cookbook not found, create new cookbook from title
            new_book = Book.objects.create(title=request.POST['book'])
            book_query = new_book
        if len(request.POST['title']) > 0:
            to_edit.title = request.POST['title']
        if len(request.POST['desc']) > 0:
            to_edit.description = request.POST['desc']
        if len(request.POST['book']) > 0:
            to_edit.book = book_query
        if len(request.POST['notes']) > 0:
            to_edit.notes = request.POST['notes']
        if request.FILES.get('photo', False):
            pic = request.FILES['photo']
            fs = FileSystemStorage()
            new_photo = fs.save(pic.name, pic)
            url = fs.url(new_photo)
            to_edit.photo = url
        to_edit.rating = request.POST['rating']
        to_edit.save()
    # elif request.method == "POST":
    #     # Without File upload
    #     # retrieve working recipe and cookbook
    #     to_edit = Recipe.objects.get(id=id)
    #     book_query = Book.objects.filter(title=request.POST['book'])
    #     if len(book_query) > 0:
    #         book_query = book_query[0]
    #     else:
    #         # If cookbook not found, create new cookbook from title
    #         new_book = Book.objects.create(title=request.POST['book'])
    #         book_query = new_book
    #     if len(request.POST['title']) > 0:
    #         to_edit.title = request.POST['title']
    #     if len(request.POST['desc']) > 0:
    #         to_edit.description = request.POST['desc']
    #     if len(request.POST['book']) > 0:
    #         to_edit.book = book_query
    #     if len(request.POST['notes']) > 0:
    #         to_edit.notes = request.POST['notes']
    #     to_edit.save()
    return redirect('/profile/'+str(request.session['id']))


# Delete selected recipe
def delete_recipe(request, id):
    if request.method == "POST":
        to_delete = Recipe.objects.get(id=id)
        to_delete.delete()
        print(f'recipe #{id} has been deleted')
        return redirect('/profile/'+str(request.session['id']))




