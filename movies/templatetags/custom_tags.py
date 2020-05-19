from django import template
from ..models import Profile

register = template.Library()

@register.filter
def isAdmin(user):
    profile = Profile.objects.get(user=user)
    return profile.is_admin

@register.filter
def is_liked(movie, profile):
    if profile is None:
        return False
    else:
        result = profile.liked_movies.filter(pk=movie.pk).first()    
        if result is None:
            return False
        else:
            return True

@register.filter
def is_watched(movie, profile):
    if profile is None:
        return False
    else:
        result = profile.watchedlist.filter(pk=movie.pk).first()    
        if result is None:
            return False
        else:
            return True  

@register.filter
def is_added(movie, profile):
    if profile is None:
        return False
    else:
        result = profile.watchlist.filter(pk=movie.pk).first()    
        if result is None:
            return False
        else:
            return True          

@register.filter
def is_commentliked(comment, user):
    if user is None:
        return False
    else:
        result = comment.commentlike.filter(pk=user.pk).first()    
        if result is None:
            return False
        else:
            return True     

@register.filter
def is_commentdisliked(comment, user):
    if user is None:
        return False
    else:
        result = comment.commentdislike.filter(pk=user.pk).first()    
        if result is None:
            return False
        else:
            return True                  

@register.filter
def is_artistliked(artist, profile):
    if profile is None:
        return False
    else:
        result = profile.liked_artists.filter(pk=artist.pk).first()    
        if result is None:
            return False
        else:
            return True 

@register.filter
def is_artistfollowed(artist, profile):
    if profile is None:
        return False
    else:
        result = profile.followed_artists.filter(pk=artist.pk).first()    
        if result is None:
            return False
        else:
            return True                                              