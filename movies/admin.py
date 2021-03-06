from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Country, Language, Genre, Occupation, MPA_Rating, Production, Artist, Movie, Franchise, Episode, Season, Series, Profile, ArtistRating, MovieRating, SeriesRating, Post

admin.site.register(Country)
admin.site.register(Language)
admin.site.register(Genre)
admin.site.register(Occupation)
admin.site.register(MPA_Rating)
admin.site.register(Production)
admin.site.register(Artist)
admin.site.register(Movie)
admin.site.register(Franchise)
admin.site.register(Episode)
admin.site.register(Season)
admin.site.register(Series)
admin.site.register(Profile)
admin.site.register(ArtistRating)
admin.site.register(MovieRating)
admin.site.register(SeriesRating)
admin.site.register(Post)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)        