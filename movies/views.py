from django.shortcuts import render, redirect
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.conf import settings
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Occupation, Staff, Genre, Movie, Profile, MovieRating, MovieComment, MovieCommentReply
import json

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

# USER ACTIONS
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

        movie = Movie.objects.create(
            name=name,
            description=description,
            plot=plot,
            runningtime=runningtime,
            release_date=release_date,
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
    context = {
        'genres': genres
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

        movie = Movie.objects.get(pk=pk)        
        movie.name = name
        movie.description = description
        movie.plot = plot
        movie.runningtime = runningtime
        movie.release_date = release_date
        movie.trailer = trailer
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
    context = {
        'genres': genres
    }

    return render(request, 'movies/movieedit.html', context)    

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
        artists = Staff.objects.filter(name__icontains=searchtext).values()
        return JsonResponse({'artists': list(artists)})
    else:
        return HttpResponse("Request method is not a GET")

def searchdirector(request):
    if request.method == 'GET':
        searchtext = request.GET.get('searchtext')
        directors = Staff.objects.filter(occupation__name='Director', name__icontains=searchtext).values()        
        return JsonResponse({'directors': list(directors)})
    else:
        return HttpResponse("Request method is not a GET")

def searchactor(request):
    if request.method == 'GET':
        searchtext = request.GET.get('searchtext')
        actors = Staff.objects.filter(occupation__name='Actor', name__icontains=searchtext).values()        
        return JsonResponse({'actors': list(actors)})
    else:
        return HttpResponse("Request method is not a GET")        

def getmoviebyid(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        movie = Movie.objects.get(id=id)
        #data = serializers.serialize('json', movie)
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
        artist = Staff.objects.get(id=id)
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

        artist = Staff.objects.create(
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

        artist = Staff.objects.get(pk=pk)        
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