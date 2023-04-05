from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vehicles, PlacaIngresando
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DetailView, ListView, DeleteView
from .forms import VehicleCreateForm
from .filters import VehicleFilter
from .serializers import VehiculoSerializer
import json
from django.shortcuts import redirect
#import lectura_placas 
from subprocess import run, PIPE
import sys

@login_required
def home(request):
    return render(request, 'DEMOAPP/home.html')


@login_required
def about(request):
    context = {
        "Vehicles": Vehicles.objects.all()
    }
    return render(request, "DEMOAPP/about.html", context)


class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicles
    template_name = 'DEMOAPP/about.html'
    context_object_name = 'Vehicles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = VehicleFilter(self.request.GET, queryset=self.get_queryset())
        return context


class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicles


@login_required
def VehicleCreateView(request):

    if request.method == 'POST':
        form = VehicleCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/parking')

    else:
        form = VehicleCreateForm()

    return render(request, 'DEMOAPP/vehicles_form.html', {'form': form})


class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicles
    success_url = '/home/parking'


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicles
    fields = ['propietario', 'placa']


@api_view(["GET"])
def IngresandoAPI(request):
    placa = PlacaIngresando.objects.first()
    serializer = VehiculoSerializer(placa, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def IngresarAPI(request):
    placa = PlacaIngresando.objects.first()
    serializer = VehiculoSerializer(instance=placa, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
'''
def external(request):
    placa_entrada = json.loads(lectura_placas.mirar_placa())
    plc = placa_entrada["placa"]
    PlacaIngresando.objects.first().update(placa=plc)
    return redirect('ingresar_auto.html')
'''