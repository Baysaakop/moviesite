from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from .models import Occupation, Artist, Genre, Movie, MPA_Rating
import json

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

def searchmovie(request):
    if request.method == 'GET':
        searchtext = request.GET.get('searchtext')
        movies = Movie.objects.filter(name__icontains=searchtext).values()
        return JsonResponse({'movies': list(movies)})
    else:
        return HttpResponse("Request method is not a GET")

def searchartist(request):
    if request.method == 'GET':
        searchtext = request.GET.get('searchtext')
        artists = Artist.objects.filter(name__icontains=searchtext).values()
        return JsonResponse({'artists': list(artists)})
    else:
        return HttpResponse("Request method is not a GET")

def searchdirector(request):
    if request.method == 'GET':
        searchtext = request.GET.get('searchtext')
        directors = Artist.objects.filter(occupation__name='Director', name__icontains=searchtext).values()        
        return JsonResponse({'directors': list(directors)})
    else:
        return HttpResponse("Request method is not a GET")

def searchactor(request):
    if request.method == 'GET':
        searchtext = request.GET.get('searchtext')
        actors = Artist.objects.filter(occupation__name='Actor', name__icontains=searchtext).values()        
        return JsonResponse({'actors': list(actors)})
    else:
        return HttpResponse("Request method is not a GET")        

def getmoviebyid(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        movie = Movie.objects.get(id=id)
        genres = serializers.serialize('json', movie.genre.all())
        directors = serializers.serialize('json', movie.director.all())
        actors = serializers.serialize('json', movie.cast.all())
        data = {
            'id': movie.id,
            'name': movie.name,
            'description': movie.description,
            'plot': movie.plot,
            'runningtime': movie.runningtime,
            'release_date': movie.release_date,
            'mpa_rating': movie.mpa_rating.id,
            'trailer': movie.trailer, 
            'image': movie.image.url,
            'poster': movie.poster.url,
            'genres': genres,
            'directors': directors,
            'actors': actors
        }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Request method is not a GET")    

def getartistbyid(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        artist = Artist.objects.get(id=id)
        occupations = serializers.serialize('json', artist.occupation.all())
        data = {
            'id': artist.id,
            'name': artist.name,
            'bio': artist.bio,
            'birthplace': artist.birthplace,
            'birthdate': artist.birthdate,
            'nationality': artist.nationality, 
            'image': artist.image.url,
            'occupations': occupations
        }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Request method is not a GET")      