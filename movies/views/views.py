from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.conf import settings
from ..models import Occupation, Artist, Genre, Movie, Profile, MovieRating, MovieComment, MovieCommentReply
from datetime import date

## Additional functions

def is_valid_queryparam(param):
    return param != '' and param is not None

def getMovieRating(movie_id):
    movie = Movie.objects.get(pk=movie_id)
    ratings = MovieRating.objects.filter(movie=movie)
    count = ratings.count()
    average = 0
    if count > 0:
        sum = 0
        for r in ratings:
            sum += r.rating
        average = sum / count
    return average

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def getBirthdate(age):
    today = date.today()
    year = today.year - age
    return date(year, today.month, today.day)


## Main views

def home(request):
    newmovies = Movie.objects.all().order_by('-updated_at')[:6]
    topratedmovies = Movie.objects.all().order_by('-rating')[:6]        
    mostlikedmovies = Movie.objects.annotate(count_liked=Count('liked_movies')).order_by('-count_liked')[:6]
    mostwatchedmovies = Movie.objects.annotate(count_watched=Count('watchedlist')).order_by('-count_watched')[:6]
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    context = {
        'newmovies': newmovies,
        'topratedmovies': topratedmovies,
        'mostlikedmovies': mostlikedmovies,
        'mostwatchedmovies': mostwatchedmovies,
        'profile': profile
    }
    return render(request, 'home.html', context)     

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)  
    favoritelist = profile.liked_movies.order_by('name')  
    watchedlist = profile.watchedlist.order_by('name')
    watchlist = profile.watchlist.order_by('name')
    context = {
        'profile': profile,
        'favoritelist': favoritelist,
        'watchedlist': watchedlist,
        'watchlist': watchlist
    }
    return render(request, 'profile.html', context)

def movielist(request):
    qs = Movie.objects.all().order_by('-updated_at')
    genres = Genre.objects.all().order_by('name')
    name = request.GET.get('name')
    releaseYearFrom = request.GET.get('releaseYearFrom')
    releaseYearTo = request.GET.get('releaseYearTo')
    genrename = request.GET.get('genrename')
    sortby = request.GET.get('sortby')

    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)

    if is_valid_queryparam(releaseYearFrom):        
        today = date.today()
        releasedate = date(int(releaseYearFrom), today.month, today.day)
        qs = qs.filter(release_date__gte=releasedate)

    if is_valid_queryparam(releaseYearTo):     
        today = date.today()
        releasedate = date(int(releaseYearTo), today.month, today.day)   
        qs = qs.filter(release_date__lt=releasedate)

    if is_valid_queryparam(genrename) and genrename != 'Choose...':
        qs = qs.filter(genre__name=genrename)

    if is_valid_queryparam(sortby):
        if sortby == 'Latest first':
            qs = qs.order_by('-updated_at')
        elif sortby == 'Latest last':
            qs = qs.order_by('updated_at')
        elif sortby == 'Rating (DESC)':
            qs = qs.order_by('-rating')
        elif sortby == 'Rating (ASC)':
            qs = qs.order_by('rating')
        elif sortby == 'Views (DESC)':
            qs = qs.order_by('-views')   
        elif sortby == 'Views (ASC)':
            qs = qs.order_by('views')        
        elif sortby == 'Release date (Newest first)':
            qs = qs.order_by('-release_date')
        elif sortby == 'Release date (Oldest first)':
            qs = qs.order_by('release_date')
        elif sortby == 'Alphabetically (A-Z)':
            qs = qs.order_by('name')
        elif sortby == 'Alphabetically (Z-A)':
            qs = qs.order_by('-name')

    count = qs.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 60)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

    context = {
        'queryset': qs,
        'genres': genres,
        'name': name,         
        'releaseYearFrom': releaseYearFrom,
        'releaseYearTo': releaseYearTo,
        'genrename': genrename,
        'sortby': sortby,
        'count': count,
        'profile': profile
    }
    return render(request, 'movies/movielist.html', context)

def moviedetail(request, pk):
    movie = Movie.objects.get(pk=pk)    
    user_rating = None
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        user_rating = MovieRating.objects.filter(user=request.user, movie=movie).first()
    comments = MovieComment.objects.filter(movie=movie).order_by('-updated_at')
    movie_rating = getMovieRating(movie.pk)    
    if user_rating is None:
        user_rating = 0
    else:
        user_rating = user_rating.rating
    context = {
        'movie': movie,
        'profile': profile,
        'user_rating': user_rating,
        'movie_rating': movie_rating,
        'comments': comments
    }
    return render(request, 'movies/moviedetail.html', context)

def artistlist(request):
    qs = Artist.objects.all().order_by('-updated_at')
    occupations = Occupation.objects.all().order_by('name')
    name = request.GET.get('name')
    occupationname = request.GET.get('occupationname')
    inputAgeMin = request.GET.get('inputAgeMin')
    inputAgeMax = request.GET.get('inputAgeMax')
    sortby = request.GET.get('sortby')    
    
    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)
    if is_valid_queryparam(occupationname) and occupationname != 'Choose...':
        qs = qs.filter(occupation__name=occupationname)
    if is_valid_queryparam(inputAgeMin):      
        datemax = getBirthdate(int(inputAgeMin))  
        qs = qs.filter(birthdate__lt=datemax)
    if is_valid_queryparam(inputAgeMax):        
        datemin = getBirthdate(int(inputAgeMax))
        qs = qs.filter(birthdate__gte=datemin)        

    if is_valid_queryparam(sortby):
        if sortby == 'Latest first':
            qs = qs.order_by('-updated_at')
        elif sortby == 'Latest last':
            qs = qs.order_by('updated_at')
        elif sortby == 'Likes (DESC)':
            qs = qs.order_by('-likes')   
        elif sortby == 'Likes (ASC)':
            qs = qs.order_by('likes')   
        elif sortby == 'Followers (DESC)':
            qs = qs.order_by('-followers')   
        elif sortby == 'Followers (ASC)':
            qs = qs.order_by('followers')   
        elif sortby == 'Alphabetically (A-Z)':
            qs = qs.order_by('name')
        elif sortby == 'Alphabetically (Z-A)':
            qs = qs.order_by('-name')

    count = qs.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 60)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

    context = {
        'queryset': qs,
        'occupations': occupations,
        'name': name,
        'occupationname': occupationname,        
        'inputAgeMin': inputAgeMin,
        'inputAgeMax': inputAgeMax,
        'sortby': sortby,
        'count': count,
        'profile': profile
    }
    return render(request, 'artists/artistlist.html', context)

def artistdetail(request, pk):
    artist = Artist.objects.get(pk=pk)
    movies = Movie.objects.filter(Q(director=artist) | Q(cast=artist)).order_by('release_date').distinct()
    movies_as_actor = Movie.objects.filter(cast=artist).order_by('release_date')
    movies_as_director = Movie.objects.filter(director=artist).order_by('release_date')      
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    context = {
        'artist': artist,
        'movies': movies,
        'movies_as_actor': movies_as_actor,
        'movies_as_director': movies_as_director,
        'profile': profile
    }
    return render(request, 'artists/artistdetail.html', context)    

