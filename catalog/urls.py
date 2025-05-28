from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_albums, name='catalogo_albums'),
    path('search/',views.buscar_contenido, name='buscar_contenido'),
    # pagians detalladas de los elementos
    path('album/<int:album_id>/', views.detalle_album, name='detalle_album'),
    path('artist/<int:artist_id>/', views.detalle_artista, name='detalle_artista'),
    path('song/<int:song_id>/', views.detalle_cancion, name='detalle_cancion'),
    # formularios para crear elementos
    path('album/form/', views.form_album, name='form_album'),
    path('artist/form/', views.form_album, name='form_artista'),
    path('song/form/', views.form_album, name='form_cancion'),
]
