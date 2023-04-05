from django import forms
from .models import Vehicles


class VehicleCreateForm(forms.ModelForm):
    class Meta:
        model = Vehicles
        fields = ['propietario', 'placa']

    def clean_propietario(self):
        propietario = self.cleaned_data.get('propietario')
        if not propietario:
            raise forms.ValidationError('This field is required')
        return propietario

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if not placa:
            raise forms.ValidationError('This field is required')

        for instance in Vehicles.objects.all():
            if instance.placa == placa:
                raise forms.ValidationError(str(placa) + ' is already created')
        return placa


