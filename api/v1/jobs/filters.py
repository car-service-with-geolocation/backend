from django_filters.rest_framework import FilterSet, filters 
 
from jobs.models import Jobs

class JobsFilter(FilterSet): 
    name = filters.CharFilter(
        field_name='name', 
        lookup_expr='istartswith'
    )
 
    class Meta: 
        model = Jobs 
        fields = ('name', ) 
