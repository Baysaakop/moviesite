from django import forms
from django.forms import SelectMultiple
from tempus_dominus.widgets import DatePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Movie, Series, Artist, Genre, Country, Occupation, Season, Episode

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'description', 'plot',  
            'release_date', 'runningtime', 'mpa_rating', 
            'genre', 'country', 'language', 
            'imdb_rating', 'metascore', 'tomatometer', 
            'trailer', 'image', 'production', 
            'producer', 'director', 'writer'        
        )
        widgets = {
            'release_date': DatePicker(
                options={
                    'minDate': '1900-01-01',
                    'maxDate': '2500-01-01',
                }
            ),
            'production': SelectMultiple(
                attrs={
                    'size': '10',
                }
            ),
            'producer': SelectMultiple(
                attrs={
                    'size': '10',
                }
            ),
            'director': SelectMultiple(
                attrs={
                    'size': '20',
                }
            ),
            'writer': SelectMultiple(
                attrs={
                    'size': '20',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        ## ARTIST FILTERING
        self.fields['genre'].queryset = Genre.objects.order_by('name')   
        self.fields['producer'].queryset = Artist.objects.filter(occupation__name='Producer').order_by('name')   
        self.fields['director'].queryset = Artist.objects.filter(occupation__name='Director').order_by('name')   
        self.fields['writer'].queryset = Artist.objects.filter(occupation__name='Writer').order_by('name')   
        ## REQUIREMENT SETTING
        self.fields['runningtime'].required = False
        self.fields['genre'].required = False
        self.fields['country'].required = False
        self.fields['language'].required = False
        self.fields['imdb_rating'].required = False
        self.fields['metascore'].required = False
        self.fields['tomatometer'].required = False
        self.fields['production'].required = False
        self.fields['producer'].required = False
        self.fields['director'].required = False
        self.fields['writer'].required = False


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ('name', 'description', 'plot',  
            'release_date', 'runningtime', 'mpa_rating', 
            'genre', 'country', 'language', 
            'imdb_rating', 'metascore', 'tomatometer', 
            'trailer', 'image', 'production', 
            'producer', 'director', 'writer'
        )
        widgets = {
            'release_date': DatePicker(
                options={
                    'minDate': '1900-01-01',
                    'maxDate': '2500-01-01',
                }
            ),
            'production': SelectMultiple(
                attrs={
                    'size': '10',
                }
            ),
            'producer': SelectMultiple(
                attrs={
                    'size': '10',
                }
            ),
            'director': SelectMultiple(
                attrs={
                    'size': '20',
                }
            ),
            'writer': SelectMultiple(
                attrs={
                    'size': '20',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SeriesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['genre'].queryset = Genre.objects.order_by('name')   
        self.fields['producer'].queryset = Artist.objects.filter(occupation__name='Producer').order_by('name')   
        self.fields['director'].queryset = Artist.objects.filter(occupation__name='Director').order_by('name')   
        self.fields['writer'].queryset = Artist.objects.filter(occupation__name='Writer').order_by('name')  
        ## REQUIREMENT SETTING
        self.fields['runningtime'].required = False
        self.fields['genre'].required = False
        self.fields['country'].required = False
        self.fields['language'].required = False
        self.fields['imdb_rating'].required = False
        self.fields['metascore'].required = False
        self.fields['tomatometer'].required = False
        self.fields['production'].required = False                
        self.fields['producer'].required = False
        self.fields['director'].required = False
        self.fields['writer'].required = False

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ('name', 'number', 'description', 'plot',  
            'release_date', 'runningtime', 'mpa_rating', 
            'genre', 'country', 'language', 
            'imdb_rating', 'metascore', 'tomatometer', 
            'trailer', 'image', 'production', 
            'producer', 'director', 'writer'
        )
        widgets = {
            'release_date': DatePicker(
                options={
                    'minDate': '1900-01-01',
                    'maxDate': '2500-01-01',
                }
            ),
            'production': SelectMultiple(
                attrs={
                    'size': '10',
                }
            ),
            'producer': SelectMultiple(
                attrs={
                    'size': '10',
                }
            ),
            'director': SelectMultiple(
                attrs={
                    'size': '20',
                }
            ),
            'writer': SelectMultiple(
                attrs={
                    'size': '20',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SeasonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['genre'].queryset = Genre.objects.order_by('name')   
        self.fields['producer'].queryset = Artist.objects.filter(occupation__name='Producer').order_by('name')   
        self.fields['director'].queryset = Artist.objects.filter(occupation__name='Director').order_by('name')   
        self.fields['writer'].queryset = Artist.objects.filter(occupation__name='Writer').order_by('name')  
        ## REQUIREMENT SETTING
        self.fields['runningtime'].required = False
        self.fields['genre'].required = False
        self.fields['country'].required = False
        self.fields['language'].required = False
        self.fields['imdb_rating'].required = False
        self.fields['metascore'].required = False
        self.fields['tomatometer'].required = False
        self.fields['production'].required = False                
        self.fields['producer'].required = False
        self.fields['director'].required = False
        self.fields['writer'].required = False

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ('name', 'number', 'description', 'plot',  
            'release_date', 'runningtime', 'mpa_rating', 
            'genre', 'country', 'language', 
            'imdb_rating', 'metascore', 'tomatometer', 
            'trailer', 'image', 'production', 
            'producer', 'director', 'writer'
        )
        widgets = {
            'release_date': DatePicker(
                options={
                    'minDate': '1900-01-01',
                    'maxDate': '2500-01-01',
                }
            ),
            'production': SelectMultiple(
                attrs={
                    'size': '10',
                }
            ),
            'producer': SelectMultiple(
                attrs={
                    'size': '10',
                }
            ),
            'director': SelectMultiple(
                attrs={
                    'size': '20',
                }
            ),
            'writer': SelectMultiple(
                attrs={
                    'size': '20',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EpisodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['genre'].queryset = Genre.objects.order_by('name')   
        self.fields['producer'].queryset = Artist.objects.filter(occupation__name='Producer').order_by('name')   
        self.fields['director'].queryset = Artist.objects.filter(occupation__name='Director').order_by('name')   
        self.fields['writer'].queryset = Artist.objects.filter(occupation__name='Writer').order_by('name')  
        ## REQUIREMENT SETTING
        self.fields['runningtime'].required = False
        self.fields['genre'].required = False
        self.fields['country'].required = False
        self.fields['language'].required = False
        self.fields['imdb_rating'].required = False
        self.fields['metascore'].required = False
        self.fields['tomatometer'].required = False
        self.fields['production'].required = False                
        self.fields['producer'].required = False
        self.fields['director'].required = False
        self.fields['writer'].required = False

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('name', 'firstname', 'lastname','bio', 
            'birthdate',  'occupation', 'country', 'image'
        )
        widgets = {
            'birthdate': DatePicker(
                options={
                    'minDate': '1800-01-01',
                    'maxDate': '3000-01-01',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        ## ARTIST FILTERING
        self.fields['occupation'].queryset = Occupation.objects.order_by('name')           
        ## REQUIREMENT SETTING
        self.fields['birthdate'].required = False
        self.fields['occupation'].required = False
        self.fields['country'].required = False
        self.fields['image'].required = False  
