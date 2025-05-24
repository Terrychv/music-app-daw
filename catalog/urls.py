from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_albums, name='catalogo_albums'),
]
