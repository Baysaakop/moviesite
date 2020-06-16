from django import template
from ..models import Profile, Series, Season, Episode

register = template.Library()

@register.filter
def is_favorite(series, profile):
    if profile is None:
        return False
    else:
        result = profile.series_favorite.filter(pk=series.pk).first()    
        if result is None:
            return False
        else:
            return True

@register.filter
def is_watched(series, profile):
    if profile is None:
        return False
    else:
        result = profile.series_watched.filter(pk=series.pk).first()    
        if result is None:
            return False
        else:
            return True  

@register.filter
def is_watchlisted(series, profile):
    if profile is None:
        return False
    else:
        result = profile.series_watchlist.filter(pk=series.pk).first()    
        if result is None:
            return False
        else:
            return True          


@register.simple_tag
def get_seasons(*args):
    seasons = Season.objects.filter(series=args[0])
    return seasons

@register.simple_tag
def get_episodes(*args):
    episodes = Episode.objects.filter(season=args[0])
    return episodes
            