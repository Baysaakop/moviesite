from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from datetime import datetime
from django.contrib.auth.models import User
from .models import Movie, Profile, MovieRating, MovieComment, MovieCommentReply

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
        
        total_likes = Profile.objects.filter(liked_movies=movie).count()
        movie.likes = total_likes
        movie.save()

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
        
        total_watched = Profile.objects.filter(watchedlist=movie).count()
        movie.watched = total_watched
        movie.save()

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

        total_watchlist = Profile.objects.filter(watchlist=movie).count()
        movie.watchlisted = total_watchlist
        movie.save()
        
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
        movie.score = average
        movie.save()
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