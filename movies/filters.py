from django.contrib.auth.models import User
from .models import Series
import django_filters

class SeriesFilter(django_filters.FilterSet):
    class Meta:
        model = Series
        fields = ['name']
