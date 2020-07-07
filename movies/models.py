from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Country(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='country_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='country_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='language_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='language_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='occupation_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='occupation_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Production(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='production_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='production_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birthdate = models.DateField(auto_now=False, blank=True, null=True)
    country = models.ManyToManyField(Country)
    occupation = models.ManyToManyField(Occupation)    
    likes = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)    
    score = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='artist_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='artist_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)        
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='genre_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='genre_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class MPA_Rating(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='mpa_rating_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='mpa_rating_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    runningtime = models.IntegerField(default=90)
    release_date = models.DateField(auto_now=False, blank=True, null=True)
    country = models.ManyToManyField(Country)
    language = models.ManyToManyField(Language)
    mpa_rating = models.ForeignKey(MPA_Rating, on_delete=models.CASCADE, blank=True, null=True)
    production = models.ManyToManyField(Production)
    producer = models.ManyToManyField(Artist, related_name='movieproducer')  
    director = models.ManyToManyField(Artist, related_name='moviedirector')    
    writer = models.ManyToManyField(Artist, related_name='moviewriter')  
    maincast = models.ManyToManyField(Artist, related_name='moviecast')
    supportingcast = models.ManyToManyField(Artist, related_name='moviesupportingcast')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)    
    watched = models.IntegerField(default=0)    
    watchlisted = models.IntegerField(default=0)    
    score = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)    
    metascore = models.IntegerField(default=0)
    tomatometer = models.IntegerField(default=0)
    image = models.ImageField(upload_to='movies/images/', blank=True, null=True)    
    trailer = models.FileField(upload_to='movies/trailers/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='movie_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='movie_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name     

class Franchise(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    runningtime = models.IntegerField(default=90)
    release_date = models.DateField(auto_now=False, blank=True, null=True)
    country = models.ManyToManyField(Country)
    language = models.ManyToManyField(Language)
    mpa_rating = models.ForeignKey(MPA_Rating, on_delete=models.CASCADE, blank=True, null=True)
    trailer = models.URLField(max_length=200, blank=True, null=True)
    production = models.ManyToManyField(Production)
    producer = models.ManyToManyField(Artist, related_name='franchiseproducer')  
    director = models.ManyToManyField(Artist, related_name='franchisedirector')    
    writer = models.ManyToManyField(Artist, related_name='franchisewriter')  
    maincast = models.ManyToManyField(Artist, related_name='franchisecast')
    supportingcast = models.ManyToManyField(Artist, related_name='franchisesupportingcast')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)    
    watched = models.IntegerField(default=0)    
    watchlisted = models.IntegerField(default=0)    
    score = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)    
    metascore = models.IntegerField(default=0)
    tomatometer = models.IntegerField(default=0)
    image = models.ImageField(upload_to='franchises/images/', blank=True, null=True)    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='franchise_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='franchise_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name

class Series(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    release_date = models.DateField(auto_now=False, blank=True, null=True)
    runningtime = models.IntegerField(default=90)
    country = models.ManyToManyField(Country)
    language = models.ManyToManyField(Language)
    mpa_rating = models.ForeignKey(MPA_Rating, on_delete=models.CASCADE, blank=True, null=True)
    production = models.ManyToManyField(Production)
    producer = models.ManyToManyField(Artist, related_name='seriesproducer')    
    director = models.ManyToManyField(Artist, related_name='seriesdirector')    
    writer = models.ManyToManyField(Artist, related_name='serieswriter')  
    maincast = models.ManyToManyField(Artist, related_name='seriesmaincast')
    supportingcast = models.ManyToManyField(Artist, related_name='seriessupportingcast')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)    
    watched = models.IntegerField(default=0)    
    watchlisted = models.IntegerField(default=0)    
    score = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)    
    metascore = models.IntegerField(default=0)
    tomatometer = models.IntegerField(default=0)
    image = models.ImageField(upload_to='series/images/', blank=True, null=True)    
    trailer = models.FileField(upload_to='series/trailers/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='series_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='series_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField(default=0)    
    description = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    runningtime = models.IntegerField(default=90)
    release_date = models.DateField(auto_now=False, blank=True, null=True)
    country = models.ManyToManyField(Country)
    language = models.ManyToManyField(Language)
    mpa_rating = models.ForeignKey(MPA_Rating, on_delete=models.CASCADE, blank=True, null=True)
    trailer = models.URLField(max_length=200, blank=True, null=True)
    production = models.ManyToManyField(Production)
    producer = models.ManyToManyField(Artist, related_name='seasonproducer')  
    director = models.ManyToManyField(Artist, related_name='seasondirector')    
    writer = models.ManyToManyField(Artist, related_name='seasonwriter')  
    maincast = models.ManyToManyField(Artist, related_name='seasonmaincast')
    supportingcast = models.ManyToManyField(Artist, related_name='seasonsupportingcast')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)    
    watched = models.IntegerField(default=0)    
    watchlisted = models.IntegerField(default=0)    
    score = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)    
    metascore = models.IntegerField(default=0)
    tomatometer = models.IntegerField(default=0)
    image = models.ImageField(upload_to='season/images/', blank=True, null=True)    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='season_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='season_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.series.name + "-" + self.name

class Episode(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField(default=0)    
    description = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    runningtime = models.IntegerField(default=90)
    release_date = models.DateField(auto_now=False, blank=True, null=True)
    country = models.ManyToManyField(Country)
    language = models.ManyToManyField(Language)
    mpa_rating = models.ForeignKey(MPA_Rating, on_delete=models.CASCADE, blank=True, null=True)
    trailer = models.URLField(max_length=200, blank=True, null=True)
    production = models.ManyToManyField(Production)
    producer = models.ManyToManyField(Artist, related_name='episodeproducer')  
    director = models.ManyToManyField(Artist, related_name='episodedirector')    
    writer = models.ManyToManyField(Artist, related_name='episodewriter')  
    maincast = models.ManyToManyField(Artist, related_name='episodemaincast')
    supportingcast = models.ManyToManyField(Artist, related_name='episodesupportingcast')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)    
    watched = models.IntegerField(default=0)    
    watchlisted = models.IntegerField(default=0)    
    score = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)    
    metascore = models.IntegerField(default=0)
    tomatometer = models.IntegerField(default=0)
    image = models.ImageField(upload_to='episode/images/', blank=True, null=True)    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='episode_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='episode_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()   

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)        
    movie_favorite = models.ManyToManyField(Movie, related_name='movie_favorite')
    movie_watched = models.ManyToManyField(Movie, related_name='movie_watched')
    movie_watchlist = models.ManyToManyField(Movie, related_name='movie_watchlist')
    series_favorite = models.ManyToManyField(Series, related_name='series_favorite')
    series_watched = models.ManyToManyField(Series, related_name='series_watched')
    series_watchlist = models.ManyToManyField(Series, related_name='series_watchlist')
    artist_favorite = models.ManyToManyField(Artist, related_name='artist_favorite')
    artist_followed = models.ManyToManyField(Artist, related_name='artist_followed')
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username

class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username + " on " + movie.name

class SeriesRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username + " on " + series.name

class ArtistRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username + " on " + artist.name