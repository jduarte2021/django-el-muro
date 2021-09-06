from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('wall/', views.wall),
    path('registro/', views.registro),
    path('login/', views.login),
    path('logout/', views.logout),
    path('mensaje/', views.mensaje),
    path('comentario/', views.comentario),
]
