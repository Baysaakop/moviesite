from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Occupation, Staff, Genre, Movie

def home(request):
    return render(request, 'home.html', {}) 

def is_valid_queryparam(param):
    return param != '' and param is not None

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
        if sortby == 'Latest':
            qs = qs.order_by('-updated_at')
        elif sortby == 'Views':
            qs = qs.order_by('-views')
        elif sortby == 'Rating':
            qs = qs.order_by('-rating')
        elif sortby == 'Release date':
            qs = qs.order_by('-release_date')
        elif sortby == 'Alphabetically':
            qs = qs.order_by('name')

    count = qs.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 32)

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
         # 'actor': actor_contains_query,
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