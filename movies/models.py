from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Occupation(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Staff(models.Model):
    name = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birthdate = models.DateField(auto_now=False, blank=True, null=True)
    birthplace = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.ManyToManyField(Occupation)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)        
    description = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    runningtime = models.IntegerField(default=90)
    release_date = models.DateField(auto_now=False, blank=True, null=True)    
    director = models.ManyToManyField(Staff, related_name='director')    
    cast = models.ManyToManyField(Staff, related_name='cast')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)    
    rating = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    image = models.ImageField(upload_to='movies/', blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    watchlist = models.ManyToManyField(Movie, related_name='watchlist')
    watchedlist = models.ManyToManyField(Movie, related_name='watchedlist')
    liked_movies = models.ManyToManyField(Movie, related_name='liked_movies')
    followed_artists = models.ManyToManyField(Staff)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()        

class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " on " + self.movie.name

class MovieComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text_comment = models.TextField()        
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " on " + self.movie.name

class MovieCommentReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_comment = models.ForeignKey(MovieComment, on_delete=models.CASCADE)
    text_comment = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " on " + self.movie.name
    
