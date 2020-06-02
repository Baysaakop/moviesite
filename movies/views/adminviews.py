from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Occupation, Artist, Genre, Movie, MPA_Rating, Series, Season, Episode, Country, Language, Profile
from ..forms import SeriesForm
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

@login_required
def seriesadd(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        plot = request.POST['plot']
        runningtime = request.POST['runningtime']
        release_date = request.POST['release_date']  
        country = request.POST['country']
        language = request.POST['lang']        
        imdb_rating = request.POST['imdb_rating']
        metascore = request.POST['metascore']  
        genres = request.POST.getlist('genre')
        trailer = request.POST['trailer']
        image = request.FILES['image']          
        productions = request.POST.getlist('production')
        producers = request.POST.getlist('producer')
        directors = request.POST.getlist('director')
        writers = request.POST.getlist('writer')
        actors = request.POST.getlist('actor')
        supportingactors = request.POST.getlist('supportingactor')
        user = request.user
        mpa_rating = request.POST['mpa_rating']
        mpa = MPA_Rating.objects.get(pk=mpa_rating)

        series = Series.objects.create(
            name=name,
            description=description,
            plot=plot,
            runningtime=runningtime,
            release_date=release_date,       
            imdb_rating=imdb_rating,
            metascore=metascore,     
            mpa_rating=mpa,
            trailer=trailer,
            image=image,
            updated_by=user
        )
        series.save()        

        c = Country.objects.filter(name=country).first()
        series.country.add(c)

        l = Language.objects.filter(name=language).first()
        series.language.add(l)

        for g in genres:
            series.genre.add(g)

        for p in productions:
            series.production.add(p)

        for p in producers:
            series.producer.add(p)

        for d in directors:
            series.director.add(d)

        for w in writers:
            series.writer.add(w)

        for a in actors:
            series.maincast.add(a)  

        for s in supportingactors:
            series.supportingcast.add(s)        

        return redirect('home')
    
    countries = Country.objects.all().order_by('name')    
    langs = Language.objects.all().order_by('name')    
    genres = Genre.objects.all().order_by('name')    
    mpa_ratings = MPA_Rating.objects.all()
    context = {
        'countries': countries,
        'genres': genres,
        'langs': langs,
        'mpa_ratings': mpa_ratings
    }
    return render(request, 'series/seriesadd.html', context)        

def is_valid_queryparam(param):
    return param != '' and param is not None

class SeriesListView(ListView):
    model = Series
    template_name = 'series/serieslist.html'
    context_object_name = 'queryset'
    paginate_by = 24
    ordering = ['-updated_at']    

    def get_context_data(self, **kwargs):
        genres = Genre.objects.all().order_by('name')        
        profile = None
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['genres'] = genres
        context['profile'] = profile
        context['name'] = self.request.GET.get('name')
        context['genrename'] = self.request.GET.get('genrename')
        context['sortby'] = self.request.GET.get('sortby')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        genrename = self.request.GET.get('genrename')
        sortby = self.request.GET.get('sortby')
        if is_valid_queryparam(name):
            queryset = queryset.filter(name__icontains=name)        
        if is_valid_queryparam(genrename) and genrename != 'Any' and genrename != 'Бүх':
            queryset = queryset.filter(genre__name=genrename)
        if is_valid_queryparam(sortby):
            if sortby == 'Latest':
                queryset = queryset.order_by('-updated_at')
            elif sortby == 'IMDB Rating':
                queryset = queryset.order_by('-imdb_rating')
            elif sortby == 'Metascore':
                queryset = queryset.order_by('-metascore')
            elif sortby == 'Views':
                queryset = queryset.order_by('-views')          
            elif sortby == 'Release date (Newest first)':
                queryset = queryset.order_by('-release_date')
            elif sortby == 'Release date (Oldest first)':
                queryset = queryset.order_by('release_date')
            elif sortby == 'Alphabetically (A-Z)':
                queryset = queryset.order_by('name')
            elif sortby == 'Alphabetically (Z-A)':
                queryset = queryset.order_by('-name')
        return queryset

class SeriesDetailView(DetailView):
    model = Series
    template_name = 'series/seriesdetail.html'
    context_object_name = 'series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context

class SeriesCreateView(CreateView):
    model = Series
    template_name = 'series/seriescreate.html'
    form_class = SeriesForm
    success_url = reverse_lazy('serieslist')    

class SeriesUpdateView(UpdateView):
    model = Series
    template_name = 'series/seriesupdate.html'
    form_class = SeriesForm    
    success_url = reverse_lazy('serieslist')    

class SeriesDeleteView(DeleteView):
    model = Series
    template_name = 'series/seriesdelete.html'
    success_url = reverse_lazy('serieslist')