from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from datetime import datetime
from django.contrib.auth.models import User
from ..models import Movie, Series, Profile, MovieRating, SeriesRating

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

def getSeriesRating(series_id):
    series = Series.objects.get(pk=series_id)
    ratings = SeriesRating.objects.filter(series=series)
    count = ratings.count()
    average = 0
    if count > 0:
        sum = 0
        for r in ratings:
            sum += r.rating
        average = sum / count
    return average

## USER ACTIONS
@login_required
def movieaddfavorite(request):
    if request.method == 'GET':
        is_liked = False
        user = request.user
        movie_id = request.GET.get('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        profile = Profile.objects.get(user=user)
        result = profile.movie_favorite.filter(pk=movie_id).first()        
        if result is None:
            profile.movie_favorite.add(movie)
            is_liked = True
        else:
            profile.movie_favorite.remove(movie)
            is_liked = False
        
        total_likes = Profile.objects.filter(movie_favorite=movie).count()
        movie.likes = total_likes
        movie.save()

        data = {
            'is_liked': is_liked
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")

@login_required
def movieaddwatched(request):
    if request.method == 'GET':
        is_watched = False
        user = request.user
        movie_id = request.GET.get('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        profile = Profile.objects.get(user=user)
        result = profile.movie_watched.filter(pk=movie_id).first()        
        if result is None:
            profile.movie_watched.add(movie)
            is_watched = True
        else:
            profile.movie_watched.remove(movie)
            is_watched = False
        
        total_watched = Profile.objects.filter(movie_watched=movie).count()
        movie.watched = total_watched
        movie.save()

        data = {
            'is_watched': is_watched
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")

@login_required
def movieaddwatchlist(request):
    if request.method == 'GET':
        is_added = False
        user = request.user
        movie_id = request.GET.get('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        profile = Profile.objects.get(user=user)
        result = profile.movie_watchlist.filter(pk=movie_id).first()        
        if result is None:
            profile.movie_watchlist.add(movie)
            is_added = True
        else:
            profile.movie_watchlist.remove(movie)
            is_added = False

        total_watchlist = Profile.objects.filter(movie_watchlist=movie).count()
        movie.watchlisted = total_watchlist
        movie.save()
        
        data = {
            'is_added': is_added
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")        

@login_required
def moviegiverating(request):
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
def seriesaddfavorite(request):
    if request.method == 'GET':
        is_liked = False
        user = request.user
        series_id = request.GET.get('series_id')
        series = Series.objects.get(pk=series_id)
        profile = Profile.objects.get(user=user)
        result = profile.series_favorite.filter(pk=series_id).first()        
        if result is None:
            profile.series_favorite.add(series)
            is_liked = True
        else:
            profile.series_favorite.remove(series)
            is_liked = False
        
        total_likes = Profile.objects.filter(series_favorite=series).count()
        series.likes = total_likes
        series.save()

        data = {
            'is_liked': is_liked
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")

@login_required
def seriesaddwatched(request):
    if request.method == 'GET':
        is_watched = False
        user = request.user
        series_id = request.GET.get('series_id')
        series = Series.objects.get(pk=series_id)
        profile = Profile.objects.get(user=user)
        result = profile.series_watched.filter(pk=series_id).first()        
        if result is None:
            profile.series_watched.add(series)
            is_watched = True
        else:
            profile.series_watched.remove(series)
            is_watched = False
        
        total_watched = Profile.objects.filter(series_watched=series).count()
        series.watched = total_watched
        series.save()

        data = {
            'is_watched': is_watched
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")

@login_required
def seriesaddwatchlist(request):
    if request.method == 'GET':
        is_added = False
        user = request.user
        series_id = request.GET.get('series_id')
        series = Series.objects.get(pk=series_id)
        profile = Profile.objects.get(user=user)
        result = profile.series_watchlist.filter(pk=series_id).first()        
        if result is None:
            profile.series_watchlist.add(series)
            is_added = True
        else:
            profile.series_watchlist.remove(series)
            is_added = False

        total_watchlist = Profile.objects.filter(series_watchlist=series).count()
        series.watchlisted = total_watchlist
        series.save()
        
        data = {
            'is_added': is_added
        }
        return JsonResponse(data)

    else:
        return HttpResponse("Request method is not a GET")        

@login_required
def seriesgiverating(request):
    if request.method == 'GET':
        user = request.user
        rating = request.GET.get('rating')
        series_id = request.GET.get('series_id')        
        series = Series.objects.get(pk=series_id)
        result = SeriesRating.objects.filter(series=series, user=user).first()
        if result is None:
            result = SeriesRating.objects.create(
                series = series,
                user = user,
                rating = rating
            )
        else:
            result.rating = rating
            result.save()
        average = getSeriesRating(series_id)
        series.score = average
        series.save()
        data = {
            'average': average
        }
        return JsonResponse(data)
    else:
        return HttpResponse("Request method is not a GET")


# @login_required
# def postComment(request):
#     if request.method == 'GET':
#         user = request.user
#         movie_id = request.GET.get('movie_id')
#         movie = Movie.objects.get(pk=movie_id)
#         textcomment = request.GET.get('textcomment')
#         moviecomment = MovieComment.objects.create(
#             user = user,
#             movie = movie,
#             text_comment = textcomment
#         )
#         count_comments = MovieComment.objects.filter(movie=movie).count()
#         data = {
#             'username': user.username,
#             'textcomment': textcomment,
#             #'updated_at': moviecomment.updated_at.strftime('%B %d, %Y'),
#             'updated_at': moviecomment.updated_at,
#             'count_comments': count_comments
#         }
#         return JsonResponse(data)

#     else:
#         return HttpResponse("Request method is not a GET")

# @login_required
# def commentLike(request):
#     if request.method == 'GET':
#         is_liked = False
#         user = request.user
#         comment_id = request.GET.get('comment_id')
#         comment = MovieComment.objects.get(pk=comment_id)
#         result = comment.moviecommentlike.filter(pk=user.pk).first()                
#         if result is None:
#             comment.moviecommentlike.add(user)
#             is_liked = True
#         else:
#             comment.moviecommentlike.remove(user)
#             is_liked = False
            
#         data = {
#             'is_liked': is_liked
#         }
#         return JsonResponse(data)

#     else:
#         return HttpResponse("Request method is not a GET")

# @login_required
# def commentDislike(request):
#     if request.method == 'GET':
#         is_disliked = False
#         user = request.user
#         comment_id = request.GET.get('comment_id')
#         comment = MovieComment.objects.get(pk=comment_id)
#         result = comment.moviecommentdislike.filter(pk=user.pk).first()                
#         if result is None:
#             comment.moviecommentdislike.add(user)
#             is_disliked = True
#         else:
#             comment.moviecommentdislike.remove(user)
#             is_disliked = False
            
#         data = {
#             'is_disliked': is_disliked
#         }
#         return JsonResponse(data)

#     else:
#         return HttpResponse("Request method is not a GET")    