from .models import PlacaIngresando
from .models import PlacaIngresando

def last_placa(request):
    return {'last_placa': PlacaIngresando.objects.all()}


