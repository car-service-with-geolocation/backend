from django_filters.rest_framework import FilterSet, filters 
 
from autoservice.models import Job

class JobsFilter(FilterSet): 
    name = filters.CharFilter(
        field_name='name', 
        lookup_expr='istartswith'
    )
 
    class Meta: 
        model = Job
        fields = ('name', ) 
