from django.urls import path
from . import views
from .views import VehicleCreateView, VehicleUpdateView, VehicleDetailView, VehicleListView, VehicleDeleteView, \
    IngresarAPI, IngresandoAPI 

urlpatterns = [
    path('', views.home, name="home-page"),
    path('parking/', VehicleListView.as_view(), name="about-page"),
    path('vehicle/new/', VehicleCreateView, name="create-page"),
    path('vehicle/<int:pk>/update/', VehicleUpdateView.as_view(), name="update-page"),
    path('vehicle/<int:pk>/delete/', VehicleDeleteView.as_view(), name="delete-page"),
    path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name="detail-page"),
    path('ingresarAPI/', IngresarAPI, name="ingresar-page"),
    path('ingresandoAPI/', IngresandoAPI, name="ingresando-page")
    #path('external/', views.external)
]
