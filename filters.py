import django_filters
from django_filters import NumberFilter
from .models import *

class DoctorFilter(django_filters.FilterSet):
    lowerBound = NumberFilter(field_name="consultation_fee", lookup_expr='gte')
    upperBound = NumberFilter(field_name="consultation_fee", lookup_expr='lte')

    class Meta:
        model = Doctor
        fields = ['specialty', 'sex', 'region']
