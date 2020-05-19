from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from datetime import datetime
from django.contrib.auth.models import User
from .models import Artist, Profile

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

# USER ACTIONS
@login_required
def likeArtist(request):
    if request.method == 'GET':
        is_liked = False
        user = request.user
        artist_id = request.GET.get('artist_id')
        artist = Artist.objects.get(pk=artist_id)
        profile = Profile.objects.get(user=user)
        result = profile.liked_artists.filter(pk=artist_id).first()        
        if result is None:
            profile.liked_artists.add(artist)
            is_liked = True
        else:
            profile.liked_artists.remove(artist)
            is_liked = False
            
        data = {
            'is_liked': is_liked
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")

@login_required
def followArtist(request):
    if request.method == 'GET':
        is_followed = False
        user = request.user
        artist_id = request.GET.get('artist_id')
        artist = Artist.objects.get(pk=artist_id)
        profile = Profile.objects.get(user=user)
        result = profile.followed_artists.filter(pk=artist_id).first()        
        if result is None:
            profile.followed_artists.add(artist)
            is_followed = True
        else:
            profile.followed_artists.remove(artist)
            is_followed = False
            
        data = {
            'is_followed': is_followed
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")

@login_required
def addToWatchlist(request):
    if request.method == 'GET':
        is_added = False
        user = request.user
        movie_id = request.GET.get('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        profile = Profile.objects.get(user=user)
        result = profile.watchlist.filter(pk=movie_id).first()        
        if result is None:
            profile.watchlist.add(movie)
            is_added = True
        else:
            profile.watchlist.remove(movie)
            is_added = False
        
        data = {
            'is_added': is_added
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")        

@login_required
def rateMovie(request):
    if request.method == 'GET':
        user = request.user
        rating = request.GET.get('rating')
        movie_id = request.GET.get('movie_id')        
        movie = Movie.objects.get(pk=movie_id)
        result = MovieRating.objects.filter(movie=movie, user=user).first()
        if result is None:
            result = MovieRating.objects.create(
                movie = movie,
                user = user,
                rating = rating
            )
        else:
            result.rating = rating
            result.save()
        average = getMovieRating(movie_id)
        data = {
            'average': average
        }
        return JsonResponse(data)
    else:
        return HttpResponse("Request method is not a GET")