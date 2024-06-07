from django.urls import path

from .views import listar_productos, agregar_producto, editar_producto, eliminar_producto
from . import views
urlpatterns = [
    # URLs de vistas normales
    path('', listar_productos, name='listar_productos'),
    path('agregar/', agregar_producto, name='agregar_producto'),
    path('<id>/editar', editar_producto, name='editar_producto'),
    path('<id>/eliminar', eliminar_producto, name='eliminar_producto'),
    path('exportar/', views.exportar_productos_csv, name='exportar_productos_csv'),
    path('importar/', views.importar_productos_csv, name='importar_productos_csv'),
]