from django.urls import path
from . import views

from django.conf.urls import handler404
from app_cata.views import handler404  # Importa tu vista personalizada

# Agrega esto al final del archivo:
handler404 = 'app_cata.views.handler404'

urlpatterns = [
    path('', views.home, name='home'),
    path('hacer-cata/', views.hacer_cata, name='hacer_cata'),
    path('cata-exitosa/', views.cata_exitosa, name='cata_exitosa'),
    path('ver-mis-catas/', views.ver_por_identificacion, name='ver_por_identificacion'),    
    path('editar-cata/<int:cata_id>/', views.editar_cata, name='editar_cata'),
    path('eliminar-cata/<int:cata_id>/', views.eliminar_cata, name='eliminar_cata'),
    path('buscar/', views.buscar_por_matricula, name='buscar_por_matricula'),


    path('mis-catas/', views.ver_mis_catas, name='ver_mis_catas'),
    path('cata/<int:cata_id>/', views.detalle_cata, name='detalle_cata'),

    ]
