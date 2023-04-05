from rest_framework import serializers
from .models import PlacaIngresando


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacaIngresando
        fields = ['placa', 'entrando']
