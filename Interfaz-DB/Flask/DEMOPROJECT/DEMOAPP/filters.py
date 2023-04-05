import django_filters
from .models import *


class VehicleFilter(django_filters.FilterSet):
    class Meta:
        model = Vehicles
        fields = ('placa',)

