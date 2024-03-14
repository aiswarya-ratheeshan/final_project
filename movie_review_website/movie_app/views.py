from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from movie_app.models import Movies, Category, FavMovies, Review


# Create your views here.
def home(request):
    obj = Movies.objects.all()
    cat_obj = Category.objects.all()
    return render(request, 'homev2.html', {'obj': obj, 'cat_obj': cat_obj})


def movie_grid_fw(request, c_slug=None):
    c_page = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        movie_list = Movies.objects.all().filter(Q(title__contains=query) | Q(category__contains=query))
    elif c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movie_list = Movies.objects.all()
    else:
        movie_list = Movies.objects.all()
    paginator = Paginator(movie_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'moviegridfw.html', {'category': c_page, 'movie': movie_list, 'products': products})


def movie_single(request, id):
    if request.method == 'POST':
        review_username = request.POST['review_username']
        review_movie = request.POST['review_movie']
        review = request.POST['review']
        review_obj = Review(username=review_username, movie=review_movie, review=review)
        review_obj.save()
    review_obj = Review.objects.all()
    fav = FavMovies.objects.all()
    movie = Movies.objects.get(id=id)
    paginator = Paginator(review_obj, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, 'moviesingle.html',
                  {'id': id, 'movie': movie, 'review_obj': review_obj, 'fav': fav, 'products': products})


def user_favorite_grid(request):
    mov_obj = Movies.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        fav_obj = FavMovies.objects.all().filter(Q(favtitle__contains=query) | Q(category__contains=query))
    else:
        fav_obj = FavMovies.objects.all()

    paginator = Paginator(fav_obj, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, 'userfavoritegrid.html', {'fav_obj': fav_obj, 'mov_obj': mov_obj, 'products': products})


def user_profile(request):
    return render(request, 'userprofile.html')


def user_rate(request):
    return render(request, 'userrate.html')


def page_not_found(request):
    return render(request, '404.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Exist")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Exist")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()
                messages.info(request, "User Registration Successfull")
                return redirect('/')
        else:
            messages.info(request, "Password Don't Match")
            return redirect('register')

    return render(request, 'homev2.html')


def login(request):
    user = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'homev2.html')


def logout(request):
    auth.logout(request)
    return render(request, 'homev2.html')


def update(request):
    if request.method == 'POST':
        update_username = request.POST['update_username']
        update_email = request.POST['update_email']
        update_firstname = request.POST['update_firstname']
        update_lastname = request.POST['update_lastname']
        update_newpass = request.POST['newpass']
        update_cnewpass = request.POST['cnewpass']
        usr = User.objects.get(username=update_username)
        usr.first_name = update_firstname
        usr.last_name = update_lastname
        usr.email = update_email
        if update_newpass == update_cnewpass:
            usr.set_password(update_newpass)
        usr.save()
    obj = Movies.objects.all()
    cat_obj = Category.objects.all()
    return render(request, 'homev2.html', {'obj': obj, 'cat_obj': cat_obj})


def add_movie(request, c_slug=None):
    cat_list = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        poster = request.FILES['poster']
        username = request.POST.get('username')
        desc = request.POST.get('description')
        release_date = request.POST.get('release_date')
        actor = request.POST.get('actor')
        director = request.POST.get('director')
        writer = request.POST.get('writer')
        category = request.POST.get('cars')
        movie_link = request.POST.get('traile_url')

        movie = Movies(title=title, poster=poster, username=username, desc=desc, release_date=release_date, actor=actor,
                       director=director,
                       writer=writer, category=category, movie_link=movie_link)
        movie.save()
        return redirect('/')
    return render(request, 'addmovie.html', {'list': cat_list})


def delete_movie(request, id):
    movie = Movies.objects.all()
    mov = Movies.objects.get(id=id)

    fav = FavMovies.objects.all()
    cat_obj = Category.objects.all()
    for i in fav:
        if mov.title == i.favtitle:
            mov.delete()
            i.delete()
        else:
            mov.delete()
            break
    else:
        mov.delete()
    return render(request, "homev2.html", {'cat_obj': cat_obj, 'movie': movie})


def edit_movie(request, id):
    obj = Movies.objects.get(id=id)
    cat_obj = Category.objects.all()
    if request.method == 'POST':
        edittitle = request.POST['edittitle']
        editposter = request.FILES['editposter']
        editusername = request.POST['editusername']
        editdescription = request.POST['editdescription']
        editrelease_date = request.POST['editrelease_date']
        editdirector = request.POST['editdirector']
        editwriter = request.POST['editwriter']
        editactor = request.POST['editactor']
        editcars = request.POST['editcars']
        edittraile_url = request.POST['edittraile_url']
        obj.title = edittitle
        obj.poster = editposter
        obj.username = editusername
        obj.desc = editdescription
        obj.release_date = editrelease_date
        obj.director = editdirector
        obj.writer = editwriter
        obj.actor = editactor
        obj.category = editcars
        obj.movie_link = edittraile_url
        obj.save()
    return render(request, 'editmovie.html', {'id': id, 'obj': obj, 'cat_obj': cat_obj})


def fav_movie(request, id):
    movie = Movies.objects.get(id=id)
    fav = FavMovies.objects.all()
    user = request.user
    count=0
    new=0
    for i in fav:
        if movie.title == i.favtitle and user.username != i.username:
            favtitle = movie.title
            poster = movie.poster
            user = user.username
            desc = movie.desc
            release_date = movie.release_date
            actor = movie.actor
            director = movie.director
            writer = movie.writer
            category = movie.category
            movie_link = movie.movie_link

            favmovie = FavMovies(favtitle=favtitle, poster=poster, username=user, desc=desc, release_date=release_date,
                                 actor=actor,
                                 director=director,
                                 writer=writer, category=category, movie_link=movie_link)
            favmovie.save()
            count = 0
            new = 0
            break
        elif user.username == i.username and movie.title != i.favtitle:
            new = 0
            count+=1
        elif user.username != i.username and movie.title != i.favtitle:
            count = 0
            new+=1
        elif user.username == i.username and movie.title == i.favtitle:
            count = 0
            new = 0
            break

    if count > 0 or new > 0:
        favtitle = movie.title
        poster = movie.poster
        user = user.username
        desc = movie.desc
        release_date = movie.release_date
        actor = movie.actor
        director = movie.director
        writer = movie.writer
        category = movie.category
        movie_link = movie.movie_link

        favmovie = FavMovies(favtitle=favtitle, poster=poster, username=user, desc=desc,
                                     release_date=release_date,
                                     actor=actor,
                                     director=director,
                                     writer=writer, category=category, movie_link=movie_link)
        favmovie.save()

    if not fav:
        favtitle = movie.title
        poster = movie.poster
        user = user.username
        desc = movie.desc
        release_date = movie.release_date
        actor = movie.actor
        director = movie.director
        writer = movie.writer
        category = movie.category
        movie_link = movie.movie_link

        favmovie = FavMovies(favtitle=favtitle, poster=poster, username=user, desc=desc, release_date=release_date,
                             actor=actor,
                             director=director,
                             writer=writer, category=category, movie_link=movie_link)
        favmovie.save()
    review_obj = Review.objects.all()
    paginator = Paginator(review_obj, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, "moviesingle.html",
                  {'id': id, 'review_obj': review_obj, 'movie': movie, 'products': products})
