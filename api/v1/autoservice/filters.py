from django_filters.rest_framework import FilterSet, filters

from autoservice.models import Job, Transport


class TransportsFilter(FilterSet):
    name = filters.CharFilter(
        field_name='brand',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Transport
        fields = ('brand', )


class JobsFilter(FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Job
        fields = ('name', )
