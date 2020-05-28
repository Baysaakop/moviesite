from django import forms
from tempus_dominus.widgets import DatePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Movie, Series, Artist

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'description', 'plot', 'genre', 'runningtime', 'release_date', 'trailer', 'image', 'director', 'cast')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save movie'))


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ('name', 'description', 'plot',  
            'release_date', 'runningtime', 'mpa_rating', 
            'genre', 'country', 'language', 
            'imdb_rating', 'metascore', 'tomatometer', 
            'trailer', 'image', 
            'production', 'producer', 
            'director', 'writer', 
            'maincast', 'supportingcast'
        )
        widgets = {
            'release_date': DatePicker(
                options={
                    'minDate': '1900-01-01',
                    'maxDate': '2500-01-01',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SeriesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        ## ARTIST FILTERING
        self.fields['producer'].queryset = Artist.objects.filter(occupation__name='Producer')
        self.fields['director'].queryset = Artist.objects.filter(occupation__name='Director')
        self.fields['writer'].queryset = Artist.objects.filter(occupation__name='Writer')
        self.fields['maincast'].queryset = Artist.objects.filter(occupation__name='Actor')
        self.fields['supportingcast'].queryset = Artist.objects.filter(occupation__name='Actor')
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
        self.fields['maincast'].required = False
        self.fields['supportingcast'].required = False