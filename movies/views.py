from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.conf import settings
from .models import Occupation, Staff, Genre, Movie, Profile, MovieRating, MovieComment, MovieCommentReply

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
    rating = request.GET.get('rating')
    release_date = request.GET.get('release_date')
    genrename = request.GET.get('genrename')
    sortby = request.GET.get('sortby')

    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)

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
        'rating': rating,
        'release_date': release_date,
        'genrename': genrename,
        'sortby': sortby,
        'count': count,
        'profile': profile
    }
    return render(request, 'movielist.html', context)

def moviedetail(request, pk):
    movie = Movie.objects.get(pk=pk)    
    total_likes = Profile.objects.filter(liked_movies=movie).count()
    total_watched = Profile.objects.filter(watchedlist=movie).count()
    total_watchlist = Profile.objects.filter(watchlist=movie).count()
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
        'total_likes': total_likes,
        'total_watched': total_watched,
        'total_watchlist': total_watchlist,
        'user_rating': user_rating,
        'movie_rating': movie_rating,
        'comments': comments
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
    paginator = Paginator(qs, 60)

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

# ACTIONS
@login_required
def likeMovie(request):
    if request.method == 'GET':
        is_liked = False
        user = request.user
        movie_id = request.GET.get('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        profile = Profile.objects.get(user=user)
        result = profile.liked_movies.filter(pk=movie_id).first()        
        if result is None:
            profile.liked_movies.add(movie)
            is_liked = True
        else:
            profile.liked_movies.remove(movie)
            is_liked = False
            
        data = {
            'is_liked': is_liked
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")

@login_required
def addToWatched(request):
    if request.method == 'GET':
        is_watched = False
        user = request.user
        movie_id = request.GET.get('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        profile = Profile.objects.get(user=user)
        result = profile.watchedlist.filter(pk=movie_id).first()        
        if result is None:
            profile.watchedlist.add(movie)
            is_watched = True
        else:
            profile.watchedlist.remove(movie)
            is_watched = False
        
        data = {
            'is_watched': is_watched
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


@login_required
def postComment(request):
    if request.method == 'GET':
        user = request.user
        movie_id = request.GET.get('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        textcomment = request.GET.get('textcomment')
        moviecomment = MovieComment.objects.create(
            user = user,
            movie = movie,
            text_comment = textcomment
        )
        count_comments = MovieComment.objects.filter(movie=movie).count()
        data = {
            'username': user.username,
            'textcomment': textcomment,
            #'updated_at': moviecomment.updated_at.strftime('%B %d, %Y'),
            'updated_at': moviecomment.updated_at,
            'count_comments': count_comments
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")

@login_required
def commentLike(request):
    if request.method == 'GET':
        is_liked = False
        user = request.user
        comment_id = request.GET.get('comment_id')
        comment = MovieComment.objects.get(pk=comment_id)
        result = comment.commentlike.filter(pk=user.pk).first()                
        if result is None:
            comment.commentlike.add(user)
            is_liked = True
        else:
            comment.commentlike.remove(user)
            is_liked = False
            
        data = {
            'is_liked': is_liked
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")

@login_required
def commentDislike(request):
    if request.method == 'GET':
        is_disliked = False
        user = request.user
        comment_id = request.GET.get('comment_id')
        comment = MovieComment.objects.get(pk=comment_id)
        result = comment.commentdislike.filter(pk=user.pk).first()                
        if result is None:
            comment.commentdislike.add(user)
            is_disliked = True
        else:
            comment.commentdislike.remove(user)
            is_disliked = False
            
        data = {
            'is_disliked': is_disliked
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")        