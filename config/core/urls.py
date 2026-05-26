from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('vendedores/', views.vendedores, name='vendedores'),
    path('clientes/', views.clientes, name='clientes'),
    path('caja/', views.caja, name='caja'),
    path('ventas/', views.ventas, name='ventas'),
    path('presupuestos/', views.presupuestos, name='presupuestos'),
    path('informes/', views.informes, name='informes'),
    path('ajustes/', views.ajustes, name='ajustes'),
]