from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from ..models import Country, Language, Genre, Occupation, MPA_Rating, Production, Artist, Movie, Episode, Season, Series, Profile, ArtistRating, MovieRating, SeriesRating
from ..forms import SeriesForm, MovieForm, ArtistForm, SeasonForm, EpisodeForm
import json

def is_valid_queryparam(param):
    return param != '' and param is not None

def getProfile(user):
    if user.is_authenticated:
        return Profile.objects.get(user=user)
    else:
        return None

def getUserMovieRating(user, movie):
    if user.is_authenticated:
        user_rating = MovieRating.objects.filter(user=user, movie=movie).first()
        if user_rating is None:
            return 0
        else:
            return user_rating.rating
    else:
        return 0

def getUserSeriesRating(user, series):
    if user.is_authenticated:
        user_rating = SeriesRating.objects.filter(user=user, series=series).first()
        if user_rating is None:
            return 0
        else:
            return user_rating.rating
    else:
        return 0

def getUserArtistRating(user, artist):
    if user.is_authenticated:
        user_rating = ArtistRating.objects.filter(user=user, artist=artist).first()
        if user_rating is None:
            return 0
        else:
            return user_rating.rating
    else:
        return 0

class MovieListView(ListView):
    model = Movie
    template_name = 'movie/movielist.html'
    context_object_name = 'queryset'
    paginate_by = 24
    count = 0
    ordering = ['-updated_at']    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = Genre.objects.all().order_by('name')        
        profile = getProfile(self.request.user)        
        context['profile'] = profile          
        context['genres'] = genres
        context['profile'] = profile
        context['name'] = self.request.GET.get('name')
        context['genrename'] = self.request.GET.get('genrename')
        context['sortby'] = self.request.GET.get('sortby')
        context['count'] = self.count
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
            elif sortby == 'Score':
                queryset = queryset.order_by('-score')
            elif sortby == 'Likes':
                queryset = queryset.order_by('-likes')
            elif sortby == 'Watched':
                queryset = queryset.order_by('-watched') 
            elif sortby == 'Watchlisted':
                queryset = queryset.order_by('-watchlisted')          
            elif sortby == 'Release date (Newest first)':
                queryset = queryset.order_by('-release_date')
            elif sortby == 'Release date (Oldest first)':
                queryset = queryset.order_by('release_date')
            elif sortby == 'Alphabetically (A-Z)':
                queryset = queryset.order_by('name')
            elif sortby == 'Alphabetically (Z-A)':
                queryset = queryset.order_by('-name') 
        self.count = queryset.count()       
        return queryset

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie/moviedetail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)      
        profile = getProfile(self.request.user)
        user_rating = getUserMovieRating(self.request.user, self.object)
        context['profile'] = profile  
        context['user_rating'] = user_rating
        return context

class MovieCreateView(CreateView):
    model = Movie
    template_name = 'movie/moviecreate.html'
    form_class = MovieForm
    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.created_by = self.request.user
        movie.save()
        form.save_m2m()
        return redirect('movielist') 

class MovieUpdateView(UpdateView):
    model = Movie
    template_name = 'movie/movieupdate.html'
    form_class = MovieForm    
    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.updated_by = self.request.user
        movie.save()
        form.save_m2m()
        return redirect('moviedetail', pk=movie.pk) 

class MovieDeleteView(DeleteView):
    model = Movie
    template_name = 'movie/moviedelete.html'
    success_url = reverse_lazy('movielist')    

class SeriesListView(ListView):
    model = Series
    template_name = 'series/serieslist.html'
    context_object_name = 'queryset'
    paginate_by = 12
    count = 0
    ordering = ['-updated_at']    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = Genre.objects.all().order_by('name')        
        profile = getProfile(self.request.user)        
        context['genres'] = genres
        context['profile'] = profile
        context['name'] = self.request.GET.get('name')
        context['genrename'] = self.request.GET.get('genrename')
        context['sortby'] = self.request.GET.get('sortby')        
        context['count'] = self.count
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
            if sortby == 'Latest' or sortby == 'Шинээр нэмэгдсэн':
                queryset = queryset.order_by('-updated_at')
            elif sortby == 'Score' or sortby == 'Үнэлгээгээр':
                queryset = queryset.order_by('-score')
            elif sortby == 'Likes' or sortby == 'Like-н тоогоор':
                queryset = queryset.order_by('-likes')
            elif sortby == 'Watched' or sortby == 'Үзсэн тоогоор':
                queryset = queryset.order_by('-watched') 
            elif sortby == 'Watchlisted' or sortby == 'Үзэхээр нэмсэн тоогоор':
                queryset = queryset.order_by('-watchlisted')          
            elif sortby == 'Release date (Newest first)' or sortby == 'Нээлтийн огноо (Шинэ нь эхэндээ)':
                queryset = queryset.order_by('-release_date')
            elif sortby == 'Release date (Oldest first)' or sortby == 'Нээлтийн огноо (Хуучин нь эхэндээ)':
                queryset = queryset.order_by('release_date')
            elif sortby == 'Alphabetically (A-Z)' or sortby == 'Үсгийн дарааллаар (А-Я)':
                queryset = queryset.order_by('name')
            elif sortby == 'Alphabetically (Z-A)' or sortby == 'Үсгийн дарааллаар (Я-А)':
                queryset = queryset.order_by('-name') 
        self.count = queryset.count()
        return queryset

class SeriesDetailView(DetailView):
    model = Series
    template_name = 'series/seriesdetail.html'
    context_object_name = 'series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        profile = getProfile(self.request.user)
        user_rating = getUserSeriesRating(self.request.user, self.object)
        context['profile'] = profile  
        context['user_rating'] = user_rating        
        return context

class SeriesCreateView(CreateView):
    model = Series
    template_name = 'series/seriescreate.html'
    form_class = SeriesForm
    def form_valid(self, form):
        series = form.save(commit=False)
        series.created_by = self.request.user
        series.save()
        form.save_m2m()
        return redirect('serieslist') 

class SeriesUpdateView(UpdateView):
    model = Series
    template_name = 'series/seriesupdate.html'
    form_class = SeriesForm    
    def form_valid(self, form):
        series = form.save(commit=False)
        series.updated_by = self.request.user
        series.save()
        form.save_m2m()
        return redirect('seriesdetail', pk=series.pk) 

class SeriesDeleteView(DeleteView):
    model = Series
    template_name = 'series/seriesdelete.html'
    success_url = reverse_lazy('serieslist')

@login_required
def season_create(request, pk):
    series = Series.objects.get(pk=pk)
    if request.method == 'POST':
        form = SeasonForm(request.POST)
        if form.is_valid():
            season = form.save(commit=False)
            season.series = series
            season.created_by = request.user
            season.save()
            form.save_m2m()
            return redirect('seriesdetail', pk=series.pk) 
    else:
        form = SeasonForm()
    context = {
        'series': series,
        'form': form
    }
    return render(request, 'season/seasoncreate.html', context)

class SeasonUpdateView(UpdateView):
    model = Season
    template_name = 'season/seasonupdate.html'
    form_class = SeasonForm    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        season = self.object
        series = season.series
        context['series'] = series
        return context

    def form_valid(self, form):
        season = form.save(commit=False)
        season.updated_by = self.request.user
        season.save()
        form.save_m2m()
        series = season.series
        return redirect('seriesdetail', pk=series.pk) 

class SeasonDeleteView(DeleteView):
    model = Season
    template_name = 'season/seasondelete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        season = self.object
        series = season.series
        context['series'] = series
        return context

    def get_success_url(self):
        season = self.object
        series = season.series
        return reverse_lazy('seriesdetail', kwargs={'pk': series.pk})

@login_required
def episode_create(request, pk):
    season = Season.objects.get(pk=pk)
    series = season.series
    if request.method == 'POST':
        form = EpisodeForm(request.POST)
        if form.is_valid():
            episode = form.save(commit=False)
            episode.season = season
            episode.created_by = request.user
            episode.save()
            form.save_m2m()
            return redirect('seriesdetail', pk=series.pk) 
    else:
        form = EpisodeForm()
    context = {
        'series': series,
        'season': season,
        'form': form
    }
    return render(request, 'episode/episodecreate.html', context)

class EpisodeUpdateView(UpdateView):
    model = Episode
    template_name = 'episode/episodeupdate.html'
    form_class = EpisodeForm    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episode = self.object
        season = episode.season
        series = season.series
        context['season'] = series
        context['series'] = series
        return context

    def form_valid(self, form):
        episode = form.save(commit=False)
        episode.updated_by = self.request.user
        episode.save()
        form.save_m2m()
        season = episode.season
        series = season.series
        return redirect('seriesdetail', pk=series.pk)   

class EpisodeDeleteView(DeleteView):
    model = Episode
    template_name = 'episode/episodedelete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episode = self.object
        season = episode.season
        series = season.series
        context['season'] = series
        context['series'] = series
        return context
        
    def get_success_url(self):
        episode = self.object
        season = episode.season
        series = season.series
        return reverse_lazy('seriesdetail', kwargs={'pk': series.pk})     

class ArtistListView(ListView):
    model = Artist
    template_name = 'artist/artistlist.html'
    context_object_name = 'queryset'
    paginate_by = 24
    count = 0
    ordering = ['-updated_at']    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        occupations = Occupation.objects.all().order_by('name')        
        profile = getProfile(self.request.user)                
        context['occupations'] = occupations
        context['profile'] = profile
        context['name'] = self.request.GET.get('name')
        context['occupationname'] = self.request.GET.get('occupationname')
        context['sortby'] = self.request.GET.get('sortby')
        context['count'] = self.count
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        occupationname = self.request.GET.get('occupationname')
        sortby = self.request.GET.get('sortby')
        if is_valid_queryparam(name):
            queryset = queryset.filter(name__icontains=name)        
        if is_valid_queryparam(occupationname) and occupationname != 'Any' and occupationname != 'Бүх':
            queryset = queryset.filter(occupation__name=occupationname)
        if is_valid_queryparam(sortby):
            if sortby == 'Latest':
                queryset = queryset.order_by('-updated_at')        
            elif sortby == 'Alphabetically (A-Z)':
                queryset = queryset.order_by('name')
            elif sortby == 'Alphabetically (Z-A)':
                queryset = queryset.order_by('-name') 
        self.count = queryset.count()       
        return queryset

class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'artist/artistdetail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        movies = Movie.objects.filter(Q(director=self.object) | Q(maincast=self.object) | Q(writer=self.object)).order_by('release_date').distinct()
        series = Series.objects.filter(Q(director=self.object) | Q(maincast=self.object) | Q(writer=self.object)).order_by('release_date').distinct()
        profile = getProfile(self.request.user)
        user_rating = getUserArtistRating(self.request.user, self.object)        
        context['movielist'] = movies
        context['serieslist'] = series
        context['profile'] = profile
        context['user_rating'] = user_rating
        return context

class ArtistCreateView(CreateView):
    model = Artist
    template_name = 'artist/artistcreate.html'
    form_class = ArtistForm
    def form_valid(self, form):
        artist = form.save(commit=False)
        artist.created_by = self.request.user
        artist.save()
        form.save_m2m()
        return redirect('artistlist')  

class ArtistUpdateView(UpdateView):
    model = Artist
    template_name = 'artist/artistupdate.html'
    form_class = ArtistForm    
    def form_valid(self, form):
        artist = form.save(commit=False)
        artist.updated_by = self.request.user
        artist.save()
        form.save_m2m()
        return redirect('artistdetail', pk=artist.pk)  

class ArtistDeleteView(DeleteView):
    model = Artist
    template_name = 'artist/artistdelete.html'
    success_url = reverse_lazy('artistlist')

def SeriesCastEdit(request, pk):
    series = Series.objects.get(pk=pk)
    if request.method == 'POST':
        maincast = request.POST.getlist('maincast')
        supportingcast = request.POST.getlist('supportingcast')
        series.maincast.clear()
        series.supportingcast.clear()
        for m in maincast:
            series.maincast.add(Artist.objects.get(pk=m))
        for s in supportingcast:
            series.supportingcast.add(Artist.objects.get(pk=s))
        series.save()
        return redirect('seriesdetail', pk=series.pk)
    else:        
        actors = Artist.objects.filter(occupation__name='Actor').order_by('name')
        context = {
            'series': series,
            'actors': actors
        }
        return render(request, 'series/seriescastedit.html', context)

def MovieCastEdit(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == 'POST':
        maincast = request.POST.getlist('maincast')
        supportingcast = request.POST.getlist('supportingcast')
        movie.maincast.clear()
        movie.supportingcast.clear()
        for m in maincast:
            movie.maincast.add(Artist.objects.get(pk=m))
        for s in supportingcast:
            movie.supportingcast.add(Artist.objects.get(pk=s))
        movie.save()
        return redirect('moviedetail', pk=movie.pk)
    else:        
        actors = Artist.objects.filter(occupation__name='Actor').order_by('name')
        context = {
            'movie': movie,
            'actors': actors
        }
        return render(request, 'movie/moviecastedit.html', context)
