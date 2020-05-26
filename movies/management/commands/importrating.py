from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from movies.models import Movie, Occupation, Genre, Artist, MPA_Rating
import csv

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='The txt file that contains the movies'
        )

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[1]                
                rated = row[3]           
                
                movie = Movie.objects.filter(name=name).first()
                mpa = MPA_Rating.objects.get_or_create(name=rated.strip()) 
                movie.mpa_rating = MPA_Rating.objects.get(name=rated.strip())              
                movie.save()                        
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))