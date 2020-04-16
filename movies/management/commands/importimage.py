from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from movies.models import Movie, Occupation, Genre, Staff
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
                name = row[0]
                image = row[1]               
                
                movie = Movie.objects.filter(name=name).first()
                movie.image = image
                movie.save()                        
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))