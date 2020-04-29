from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Occupation, Staff, Genre, Movie, Profile, MovieRating

def home(request):
    return render(request, 'home.html', {})     

def is_valid_queryparam(param):
    return param != '' and param is not None

def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

def movielist(request):
    qs = Movie.objects.all().order_by('-updated_at')
    genres = Genre.objects.all().order_by('name')
    name = request.GET.get('name')
    # actor_contains_query = request.GET.get('actor_contains')
    rating = request.GET.get('rating')
    release_date = request.GET.get('release_date')
    genrename = request.GET.get('genrename')
    sortby = request.GET.get('sortby')

    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)

    # elif is_valid_queryparam(actor_contains_query):
    #     qs = qs.filter(cast__name__icontains=actor_contains_query).distinct()

    if is_valid_queryparam(rating):        
        qs = qs.filter(rating__gte=rating)

    if is_valid_queryparam(release_date):        
        qs = qs.filter(release_date__gte=release_date)

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
    paginator = Paginator(qs, 36)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'queryset': qs,
        'genres': genres,
        'name': name,         
        'rating': rating,
        'release_date': release_date,
        'genrename': genrename,
        'sortby': sortby,
        'count': count
    }
    return render(request, 'movielist.html', context)


def moviedetail(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie': movie
    }
    return render(request, 'moviedetail.html', context)

def artistlist(request):
    qs = Staff.objects.all().order_by('name')
    occupations = Occupation.objects.all().order_by('name')
    name = request.GET.get('name')
    occupationname = request.GET.get('occupationname')
    sortby = request.GET.get('sortby')

    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)
    if is_valid_queryparam(occupationname) and occupationname != 'Choose...':
        qs = qs.filter(occupation__name=occupationname)

    if is_valid_queryparam(sortby):
        if sortby == 'Alphabetically (A-Z)':
            qs = qs.order_by('name')
        elif sortby == 'Alphabetically (Z-A)':
            qs = qs.order_by('-name')

    count = qs.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 36)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'queryset': qs,
        'occupations': occupations,
        'name': name,
        'occupationname': occupationname,
        'sortby': sortby,
        'count': count
    }
    return render(request, 'artistlist.html', context)

def artistdetail(request, pk):
    artist = Staff.objects.get(pk=pk)
    movies = Movie.objects.filter(Q(director=artist) | Q(cast=artist)).order_by('release_date').distinct()
    movies_as_actor = Movie.objects.filter(cast=artist).order_by('release_date')
    movies_as_director = Movie.objects.filter(director=artist).order_by('release_date')
    context = {
        'artist': artist,
        'movies': movies,
        'movies_as_actor': movies_as_actor,
        'movies_as_director': movies_as_director,
    }
    return render(request, 'artistdetail.html', context)    
    