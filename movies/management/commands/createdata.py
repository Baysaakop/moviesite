from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from movies.models import Movie, Occupation, Genre, Artist, Production, Country, Language, MPA_Rating
from datetime import date
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
                id = row[0]
                name = row[1]
                year = row[2]
                rated = row[3]                
                release = row[4]
                runningtime = row[5]
                genres = row[6]
                directors = row[7]
                writers = row[8]
                cast = row[9]
                plot = row[10]
                languages = row[11]
                countries = row[12]
                poster = row[13]
                metascore = row[14]
                imdb_rating = row[15]
                productions = row[16]                

                rel = release.split("/")
                release_date = date(int(rel[0]), int(rel[1]), int(rel[2]))                

                movie = Movie(
                    name = name,
                    runningtime = int(runningtime.replace("min", "")),
                    release_date = release_date,
                    plot = plot,
                    imdb_rating = float(imdb_rating),
                    metascore = int(metascore),                    
                    poster=poster                                        
                )

                movie.save()                           

                mpa = MPA_Rating.objects.get_or_create(name=rated.strip())          
                movie.mpa_rating = MPA_Rating.objects.get(name=rated.strip())              

                genrelist = genres.split(',')
                for genre in genrelist:
                    g = Genre.objects.get_or_create(name=genre.strip())                     
                    movie.genre.add(Genre.objects.get(name=genre.strip()))                         

                countrylist = countries.split(',')
                for country in countrylist:
                    c = Country.objects.get_or_create(name=country.strip())                     
                    movie.country.add(Country.objects.get(name=country.strip()))   

                languagelist = languages.split(',')
                for language in languagelist:
                    l = Language.objects.get_or_create(name=language.strip())                     
                    movie.language.add(Language.objects.get(name=language.strip()))

                productionlist = productions.split(',')
                for production in productionlist:
                    p = Production.objects.get_or_create(name=production.strip())                     
                    movie.production.add(Production.objects.get(name=production.strip()))                               

                directorlist = directors.split(',')                           
                for director in directorlist:
                    o = Occupation.objects.get(name="Director")
                    try:
                        artist = Artist.objects.get(name=director.strip())                        
                        artist.occupation.add(o)
                    except ObjectDoesNotExist:
                        artist = Artist(
                            name = director.strip()                            
                        )                                        
                        artist.save()     
                        artist.occupation.add(o)                       
                    movie.director.add(Artist.objects.get(name=director.strip()))

                writerlist = writers.split(',')
                for writer in writerlist:
                    if "(" in writer:
                        index = writer.index("(")
                        writer = writer[0:index]
                    o = Occupation.objects.get(name="Writer")
                    try:
                        artist = Artist.objects.get(name=writer.strip())                        
                        artist.occupation.add(o)
                    except ObjectDoesNotExist:
                        artist = Artist(
                            name = writer.strip()                            
                        )                                        
                        artist.save()     
                        artist.occupation.add(o)                       
                    movie.writer.add(Artist.objects.get(name=writer.strip()))

                actorlist = cast.split(',')                           
                for actor in actorlist:
                    o = Occupation.objects.get(name="Actor")
                    try:
                        artist = Artist.objects.get(name=actor.strip())
                        artist.occupation.add(o)                                            
                    except ObjectDoesNotExist:
                        artist = Artist(
                            name = actor.strip()                            
                        )                        
                        artist.save()
                        artist.occupation.add(o)
                    movie.cast.add(Artist.objects.get(name=actor.strip()))                        
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))