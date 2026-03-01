from django.urls import path
from . import views

urlpatterns = [
    path('polizas/', views.listar_polizas),
    path('polizas/<int:pk>/riesgos/', views.listar_riesgos),
    path('polizas/<int:pk>/renovar/', views.renovar_poliza),
    path('polizas/<int:pk>/cancelar/', views.cancelar_poliza),
    path('polizas/<int:pk>/riesgos/agregar/', views.agregar_riesgo),
    path('riesgos/<int:pk>/cancelar/', views.cancelar_riesgo),
    path('core-mock/evento/', views.core_mock_evento),
]