import django_filters
from .models import Movie

class MovieListFilter(django_filters.FilterSet):
    year_gt = django_filters.NumberFilter(field_name='year', lookup_expr='year__gt')
    year_lt = django_filters.NumberFilter(field_name='year', lookup_expr='year__lt')

    class Meta:
        model = Movie
        fields = {
            'country': ['exact'],
            'genre': ['exact'],
            'status_movie': ['exact'],
            'actors': ['exact'],
            'director': ['exact']
        }
