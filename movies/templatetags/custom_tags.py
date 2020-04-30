from django import template

register = template.Library()

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