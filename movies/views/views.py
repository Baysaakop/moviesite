from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.conf import settings
from django.utils import translation
from ..models import Occupation, Artist, Genre, Movie, Profile, MovieRating, Series
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
    # user_language = 'mn'
    # translation.activate(user_language)
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    latestmovies = Movie.objects.all().order_by('-created_at')[:4]
    latestseries = Series.objects.all().order_by('-created_at')[:4]
    suggestedmovie = Movie.objects.latest('created_at')
    suggestedseries = Series.objects.latest('created_at')
    # topratedmovies = Movie.objects.all().order_by('-imdb_rating')[:4]        
    # mostlikedmovies = Movie.objects.annotate(count_liked=Count('liked_movies')).order_by('-count_liked')[:6]
    # mostwatchedmovies = Movie.objects.annotate(count_watched=Count('moviewatchedlist')).order_by('-count_watched')[:6]
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    context = {
        'latestmovies': latestmovies,
        'latestseries': latestseries,
        'suggestedmovie': suggestedmovie,
        'suggestedseries': suggestedseries,
        # 'mostlikedmovies': mostlikedmovies,
        # 'mostwatchedmovies': mostwatchedmovies,
        'profile': profile
    }
    return render(request, 'home.html', context)     

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)  
    movie_favorite = profile.movie_favorite.order_by('name')  
    movie_watched = profile.movie_watched.order_by('name')
    movie_watchlist = profile.movie_watchlist.order_by('name')
    context = {
        'profile': profile,
        'movie_favorite': movie_favorite,
        'movie_watched': movie_watched,
        'movie_watchlist': movie_watchlist
    }
    return render(request, 'profile.html', context)
