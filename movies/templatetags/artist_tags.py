from django import template
from ..models import Profile

register = template.Library()

@register.filter
def is_favorite(artist, profile):
    if profile is None:
        return False
    else:
        result = profile.artist_favorite.filter(pk=artist.pk).first()    
        if result is None:
            return False
        else:
            return True

@register.filter
def is_followed(artist, profile):
    if profile is None:
        return False
    else:
        result = profile.artist_followed.filter(pk=artist.pk).first()    
        if result is None:
            return False
        else:
            return True  
 

            