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
                date = row[1]
                runningtime = row[2]
                genres = row[3]
                directors = row[4]
                writers = row[5]
                cast = row[6]
                plot = row[7]
                photo = row[8]
                rating = float(row[9])
                views = float(row[10])                

                movie = Movie(
                    name = name,
                    runningtime=int(runningtime.replace("min", "")),
                    release_date=date,
                    plot=plot,
                    rating=rating,
                    views=views,
                    photo=photo                    
                )

                movie.save()

                genrelist = genres.split(',')
                for genre in genrelist:
                     g = Genre.objects.get_or_create(name=genre.strip())                     
                     movie.genre.add(Genre.objects.get(name=genre.strip()))          

                directorlist = directors.split(',')                           
                for director in directorlist:
                    o = Occupation.objects.get(name="Director")
                    try:
                        staff = Staff.objects.get(name=director.strip())                        
                        staff.occupation.add(o)
                    except ObjectDoesNotExist:
                        staff = Staff(
                            name = director.strip()                            
                        )                                        
                        staff.save()     
                        staff.occupation.add(o)                       
                    movie.director.add(Staff.objects.get(name=director.strip()))

                actorlist = cast.split(',')                           
                for actor in actorlist:
                    o = Occupation.objects.get(name="Actor")
                    try:
                        staff = Staff.objects.get(name=actor.strip())
                        staff.occupation.add(o)                                            
                    except ObjectDoesNotExist:
                        staff = Staff(
                            name = actor.strip()                            
                        )                        
                        staff.save()
                        staff.occupation.add(o)
                    movie.cast.add(Staff.objects.get(name=actor.strip()))
                        
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))