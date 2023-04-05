from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Vehicles(models.Model):
    propietario = models.CharField(max_length=100)
    placa = models.CharField(max_length=20)
    estado = models.BooleanField(default=False)
    posicion = models.CharField(max_length=5, default="---")
    hora_ingreso = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.placa

    def get_absolute_url(self):
        return reverse('detail-page', kwargs={'pk': self.pk})


class WatchMen(models.Model):
    Nombre = models.ForeignKey(User, on_delete=models.CASCADE)


class Posicion(models.Model):
    puesto = models.JSONField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.puesto = []
        for contador1 in range(0, 9):
            self.puesto.append([])
            for contador2 in range(0, 9):
                self.puesto[contador1].append([contador2, False])


class PlacaIngresando(models.Model):
    placa = models.CharField(max_length=20)
    entrando = models.BooleanField(default=True)


parqueadero = Posicion()


@receiver(pre_save, sender=PlacaIngresando)
def ubicarVehiculo(sender, instance, **kuargs):
    contador1 = 0
    contador2 = 0
    ingreso = False
    if instance.entrando:
        for puesto in parqueadero.puesto:
            for data in puesto:
                if not data[1] and not Vehicles.objects.get(placa=instance.placa).estado:
                    Vehicles.objects.filter(placa=instance.placa).update(estado=True)
                    data[1] = True
                    ingreso = True
                    Vehicles.objects.filter(placa=instance.placa).update(posicion=str(contador1) + "-" + str(contador2))
                    break
                contador2 += 1
            if ingreso:
                print("Vehiculo ingresando")
                break
            contador1 += 1
    else:
        objeto = Vehicles.objects.filter(placa=instance.placa).values()
        x = []
        posicion1 = "0"
        posicion2 = "0"
        if Vehicles.objects.get(placa=instance.placa).estado:
            Vehicles.objects.filter(placa=instance.placa).update(estado=False)
            for data in objeto:
                x = data["posicion"].split("-")
                posicion1 = x[0]
                posicion2 = x[1]
            parqueadero.puesto[int(posicion1)][int(posicion2)][1] = False
            Vehicles.objects.filter(placa=instance.placa).update(posicion="---")
        print("Vehiculo saliendo")
