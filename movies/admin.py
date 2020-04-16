from django.contrib import admin
from .models import Occupation, Staff, Genre, Movie

admin.site.register(Occupation)
admin.site.register(Staff)
admin.site.register(Genre)
admin.site.register(Movie)