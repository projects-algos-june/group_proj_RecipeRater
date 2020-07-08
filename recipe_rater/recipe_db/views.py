from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import User, Book, Recipe, Friendship, Step, UserManager, RecipeManager
import bcrypt


"""
Page Renders for site
"""
# Log/Register page
def index(request):
    return render(request, 'index.html')


"""
Start recipe ordering
"""
"""
Recipes viewed in posted order
"""
# Renders recipes added by user
def profile(request, id):
    user_info = User.objects.get(id=id)
    context = {
        'user_recipes': user_info.posted_recipes.all(),
        'all_recipes' : Recipe.objects.all(),
        'all_books' : Book.objects.all()
    }
    return render(request, 'user_profile.html', context)
"""
Recipes viewed by name
"""
def profile_name_prioity(request, id):
    user_info = User.objects.get(id=id)
    context = {
        'user_recipes': user_info.posted_recipes.all().order_by('title')
    }
    return render(request, 'user_profile.html', context)
"""
Recipes viewed by cookbook
"""
def profile_book_priority(request, id):
    user_info = User.objects.get(id=id)
    context = {
        'user_recipes': user_info.posted_recipes.all().order_by('book')
    }
    return render(request, 'user_profile.html', context)
"""
Recipes viewed by rating
"""
def profile_rating_priority(request, id):
    user_info = User.objects.get(id=id)
    context = {
        'user_recipes': user_info.posted_recipes.all().order_by('-rating')
    }
    return render(request, 'user_profile.html', context)




def friend_profile(request, id):
    user_info = User.objects.get(id=id)
    context = {
        'curr_friend': user_info,
        'user_recipes': user_info.posted_recipes.all()
    }
    # for recipe in context['user_recipes']:
    #     print(recipe.title)
    return render(request, 'friend_profile.html', context)

def user_friends(request, id):
    context = {
        'curr_user': User.objects.get(id=id),
        'all_users' : User.objects.all(),
        'users': User.objects.exclude(id=request.session['id']),
        'friends': Friendship.objects.filter(creator=request.session['id'])
    }
    return render(request, 'user_friends.html', context)
def bookpage(request, id):
    context = {
        'cookbook': Book.objects.get(id=id),
        'all_recipes' : Recipe.objects.all()
    }
    return render(request, 'cookbook.html', context)

def allrecipes(request):
    context = {
        'all_recipes' : Recipe.objects.all()
    }
    return render(request, 'allrecipes.html', context)

# Renders form to create new recipe
def render_add_form(request):
    context = {
        'all_books': Book.objects.all()
    }
    return render(request, 'add_recipe.html', context)

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



"""
Redirect functionality of website
"""
"""
User manipulation and functionality
"""
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
            messages.error(request, 'Password was incorrect')
            return redirect('/')
        messages.error(request, 'Email address not found')
        return redirect('/')

# Flush user from request.session and return to Login page
def logout(request):
    request.session.flush()
    print("Session has been flushed")
    return redirect('/')
    



"""
Friendship management views
"""
# Add Friend
def add_friend(request, id):
    if request.method == "POST":
        curr_user = User.objects.get(id=request.session['id'])
        requested_user = User.objects.get(id=id)
        friend_query = Friendship.objects.filter(creator=curr_user, friend=requested_user)
        if len(friend_query) == 0:
            new_friend = Friendship.objects.create(
                creator = curr_user,
                friend = requested_user
            )
            print(f'{curr_user} is now friends with {new_friend.friend.first_name}')
        return redirect('/user_friends/'+str(request.session['id']))
    return redirect('/user_friends/'+str(request.session['id']))

def remove_friend(request, id):
    if request.method == "POST":
        to_remove = Friendship.objects.get(id=id)
        print(f'Friendship with {to_remove.friend.first_name} {to_remove.friend.last_name} has been removed')
        to_remove.delete()
        return redirect('/user_friends/'+str(request.session['id']))
    redirect('/user_friends/'+str(request.session['id']))


"""
Recipe views
"""
# Process form for adding recipe
def add_recipe(request):
    if request.method == "POST":
        errors = Recipe.objects.recipe_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/add_recipe')
        url = None
        print(request.session['id'])
        if request.FILES.get('photo', False):
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
                rating = 0,
                notes = request.POST['notes'],
                photo = url,
                poster = User.objects.get(id=request.session['id'])
            )
            print(f'{new_recipe.title} recipe successfully created for {new_recipe.book.title}')
            for i in range(0, int(request.POST['member'])):
                print('step'+str(i))
                Step.objects.create(recipe = new_recipe, content=request.POST['step'+str(i)])
            
        else:
            url = None
            if request.FILES.get('photo', False):
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
            else:
                new_book = Book.objects.create(title=request.POST['book'])
                book_query = new_book
            new_recipe = Recipe.objects.create(
                title = request.POST['title'],
                description = request.POST['desc'],
                book = book_query,
                rating = 0,
                notes = request.POST['notes'],
                photo = url,
                poster = User.objects.get(id=request.session['id'])
            )
            print(f'{new_recipe.title} recipe successfully created for {new_recipe.book.title}')
            for i in range(0, int(request.POST['member'])):
                print('step'+str(i))
                Step.objects.create(recipe = new_recipe, content=request.POST['step'+str(i)])
            
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
    return redirect('/profile/'+str(request.session['id']))


# Delete selected recipe
def delete_recipe(request, id):
    if request.method == "POST":
        to_delete = Recipe.objects.get(id=id)
        to_delete.delete()
        print(f'recipe #{id} has been deleted')
        return redirect('/profile/'+str(request.session['id']))


def search(request):
    if request.method == 'POST':
        results = request.POST['results']
        user_id = request.POST['profile_id']
        request.session['result'] = results
    return redirect('/profile/' + str(user_id))

def clearsearch(request, id):
    del request.session['result']
    return redirect('/profile/'+str(id))

def rating(request, id):
    if request.method == 'POST':
        recipe_rated = Recipe.objects.get(id=id)
        user_rating = User.objects.get(id=request.session['id'])
        rater_query = User.objects.filter(raters=id)
        print(rater_query)
        if len(rater_query) == 0:
            print("new user")
            recipe_rated.rated_by.add(user_rating)  
            recipe_rated.count = recipe_rated.count + 1
            recipe_rated.rating = recipe_rated.rating + int(request.POST['rate'])
            forks = recipe_rated.rating/recipe_rated.count
            if forks > 5:
                forks = 5
            recipe_rated.forks = round(forks)
            recipe_rated.save()
            return redirect('/recipe/' + str(id))
        return redirect('/recipe/' + str(id))

def friendsearch(request):
    user_id = request.POST['profile_id']
    if len(request.POST['search']) > 0:
        if request.method == 'POST':
            results = request.POST['search']          
            request.session['result'] = results
    return redirect('/user_friends/' + str(user_id))

def clearfsearch(request, id):
    del request.session['result']
    return redirect('/user_friends/'+str(id))