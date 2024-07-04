# escuelavirtual/urls.py

from django.contrib import admin
from django.urls import path, include
from actividades import views as actividades_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', actividades_views.home, name='home'),
    path('actividades/', include('actividades.urls', namespace='actividades')),  # Incluye el namespace 'actividades'
]
