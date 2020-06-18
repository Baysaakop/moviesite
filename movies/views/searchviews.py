from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from ..models import Occupation, Artist, Genre, Movie, MPA_Rating, Production, Country, Language, Series, Season, Episode
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

def search(request):
    search = request.GET.get('search', '')       
    search = search.strip().lower() 
    if search:
        usearch = search[0].upper() + search[1:len(search)]
        print(search)
        print(usearch)
        movies = Movie.objects.filter(name__icontains=search) | Movie.objects.filter(name__icontains=usearch)
        series = Series.objects.filter(name__icontains=search) | Series.objects.filter(name__icontains=usearch)
        artists = Artist.objects.filter(name__icontains=search) | Artist.objects.filter(name__icontains=usearch)
        context = {
            'movies': movies,
            'series': series,
            'artists': artists
        }                
    else:
        context = {}
    return render(request, 'search.html', context)


def searchactor(request):
    if request.method == 'GET':
        searchtext = request.GET.get('searchtext')
        actors = Artist.objects.filter(occupation__name='Actor', name__icontains=searchtext).values()        
        return JsonResponse({'actors': list(actors)})
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
            'birthdate': artist.birthdate,
            # 'image': artist.image.url,
            'occupations': occupations
        }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Request method is not a GET")      

def getproductionbyid(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        production = Production.objects.get(id=id)        
        data = {
            'id': production.id,
            'name': production.name,
        }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Request method is not a GET")    