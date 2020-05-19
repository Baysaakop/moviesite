from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from .models import Occupation, Artist, Genre, Movie, MPA_Rating
import json

## ADMIN VIEWS
@login_required
def movieadd(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        plot = request.POST['plot']
        runningtime = request.POST['runningtime']
        release_date = request.POST['release_date']        
        genres = request.POST.getlist('genre')
        trailer = request.POST['trailer']
        image = request.FILES['image']        
        poster = request.FILES['poster']      
        directors = request.POST.getlist('director')
        actors = request.POST.getlist('actor')
        user = request.user
        mpa_rating = request.POST['mpa_rating']
        mpa = MPA_Rating.objects.get(pk=mpa_rating)

        movie = Movie.objects.create(
            name=name,
            description=description,
            plot=plot,
            runningtime=runningtime,
            release_date=release_date,
            mpa_rating=mpa,
            trailer=trailer,
            image=image,
            poster=poster,
            updated_by=user
        )
        movie.save()        

        for g in genres:
            movie.genre.add(g)

        for d in directors:
            movie.director.add(d)

        for a in actors:
            movie.cast.add(a)        

        return redirect('movielist')
    
    genres = Genre.objects.all().order_by('name')    
    mpa_ratings = MPA_Rating.objects.all()
    context = {
        'genres': genres,
        'mpa_ratings': mpa_ratings
    }

    return render(request, 'movies/movieadd.html', context)

@login_required
def movieedit(request):
    if request.method == 'POST':
        pk = request.POST['id']
        name = request.POST['name']
        description = request.POST['description']
        plot = request.POST['plot']
        runningtime = request.POST['runningtime']
        release_date = request.POST['release_date']
        genres = request.POST.getlist('genre')
        trailer = request.POST['trailer']
        image = request.FILES.get('image')
        poster = request.FILES.get('poster')
        directors = request.POST.getlist('director')
        actors = request.POST.getlist('actor')
        user = request.user
        mpa_rating = request.POST['mpa_rating']
        mpa = MPA_Rating.objects.get(pk=mpa_rating)

        movie = Movie.objects.get(pk=pk)        
        movie.name = name
        movie.description = description
        movie.plot = plot
        movie.runningtime = runningtime
        movie.release_date = release_date
        movie.trailer = trailer
        movie.mpa_rating = mpa
        movie.updated_by = user    

        if image is not None:
            movie.image=image
        if poster is not None:
            movie.poster=poster            
        movie.genre.clear()
        for g in genres:
            movie.genre.add(g)
        movie.director.clear()
        for d in directors:
            movie.director.add(d)
        movie.cast.clear()
        for a in actors:
            movie.cast.add(a)                
        movie.save()
        return redirect('movielist')
    
    genres = Genre.objects.all().order_by('name')       
    mpa_ratings = MPA_Rating.objects.all()
    context = {
        'genres': genres,
        'mpa_ratings': mpa_ratings
    }

    return render(request, 'movies/movieedit.html', context)              

@login_required
def moviedelete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id is not None:
            movie = Movie.objects.get(id=id)
            movie.delete()
            return redirect('movielist')
    else:
        return HttpResponse("Request method is not a GET")

@login_required
def artistadd(request):
    if request.method == 'POST':
        name = request.POST['name']
        bio = request.POST['bio']
        birthplace = request.POST['birthplace']
        birthdate = request.POST['birthdate']
        nationality = request.POST['nationality']
        occupations = request.POST.getlist('occupation')
        image = request.FILES['image']          
        user = request.user

        artist = Artist.objects.create(
            name=name,
            bio=bio,
            birthplace=birthplace,
            birthdate=birthdate,
            nationality=nationality,
            image=image,
            updated_by=user
        )

        artist.save()
        for o in occupations:
            artist.occupation.add(o)     

        return redirect('artistlist')
    
    occupations = Occupation.objects.all().order_by('name')        
    context = {
        'occupations': occupations
    }

    return render(request, 'artists/artistadd.html', context)        

@login_required
def artistedit(request):
    if request.method == 'POST':
        pk = request.POST['id']
        name = request.POST['name']
        bio = request.POST['bio']
        birthplace = request.POST['birthplace']
        birthdate = request.POST['birthdate']
        nationality = request.POST['nationality']
        occupations = request.POST.getlist('occupation')
        image = request.FILES.get('image')     
        user = request.user

        artist = Artist.objects.get(pk=pk)        
        artist.name = name
        artist.bio = bio
        artist.birthplace = birthplace
        artist.nationality = nationality
        artist.birthdate = birthdate
        artist.updated_by = user                
        if image is not None:
            artist.image=image        
        artist.occupation.clear()
        for o in occupations:
            artist.occupation.add(o)                     
        martistovie.save()
        return redirect('artistlist')
    
    occupations = Occupation.objects.all().order_by('name')        
    context = {
        'occupations': occupations
    }

    return render(request, 'artists/artistedit.html', context)       

@login_required
def artistdelete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id is not None:
            artist = Artist.objects.get(id=id)
            artist.delete()
            return redirect('artistlist')
    else:
        return HttpResponse("Request method is not a GET")    