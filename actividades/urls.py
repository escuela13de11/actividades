# actividades/urls.py

from django.urls import path
from . import views

app_name = 'actividades'

urlpatterns = [
    path('', views.home, name='home'),
    path('superuser/superuser_view/', views.superuser_view, name='superuser_view'),
    path('<str:username>/seleccion/', views.grade_selection, name='grade_selection'),
    path('<str:username>/6to/matematica/', views.matematica_6to, name='matematica_6to'),
    path('<str:username>/6to/lengua/', views.lengua_6to, name='lengua_6to'),
    path('<str:username>/7mo/matematica/', views.matematica_7mo, name='matematica_7mo'),
    path('<str:username>/7mo/lengua/', views.lengua_7mo, name='lengua_7mo'),
    path('<str:username>/actividad1/', views.actividad1, name='actividad1'),
    path('<str:username>/actividad2/', views.actividad2, name='actividad2'),
    path('<str:username>/actividad3/', views.actividad3, name='actividad3'),
    path('<str:username>/index/', views.index, name='index'),
    path('<str:username>/6to/matematica/sistema_numeracion/', views.sistema_numeracion, name='sistema_numeracion'),
    path('corregir_actividad/', views.corregir_actividad, name='corregir_actividad'),
    path('<str:username>/6to/matematica/sistema_numeracion/', views.sistema_numeracion, name='sistema_numeracion'),
    path('multiplos_y_divisores_i/<str:username>/', views.multiplos_y_divisores_i, name='multiplos_y_divisores_i'),
]
