from django.db import models
from django.contrib.auth.models import User

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

    
