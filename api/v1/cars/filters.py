from django_filters.rest_framework import FilterSet, filters 
 
from cars.models import Transport

class TransportsFilter(FilterSet): 
    name = filters.CharFilter(
        field_name='brand', 
        lookup_expr='istartswith'
    )
 
    class Meta: 
        model = Transport 
        fields = ('brand', ) 
