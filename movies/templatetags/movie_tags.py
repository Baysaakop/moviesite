from django import template
from ..models import Profile

register = template.Library()

@register.filter
def is_favorite(movie, profile):
    if profile is None:
        return False
    else:
        result = profile.movie_favorite.filter(pk=movie.pk).first()    
        if result is None:
            return False
        else:
            return True

@register.filter
def is_watched(movie, profile):
    if profile is None:
        return False
    else:
        result = profile.movie_watched.filter(pk=movie.pk).first()    
        if result is None:
            return False
        else:
            return True  

@register.filter
def is_watchlisted(movie, profile):
    if profile is None:
        return False
    else:
        result = profile.movie_watchlist.filter(pk=movie.pk).first()    
        if result is None:
            return False
        else:
            return True          