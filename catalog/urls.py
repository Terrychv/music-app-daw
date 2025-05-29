from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_albums, name='catalogo_albums'),
    path('search/',views.buscar_contenido, name='buscar_contenido'),
    path('top_albums/', views.top_albums, name='top_albums'),
    path('top_canciones/', views.top_canciones, name='top_canciones'),
    # pagians detalladas de los elementos
    path('album/<int:album_id>/', views.detalle_album, name='detalle_album'),
    path('artist/<int:artist_id>/', views.detalle_artista, name='detalle_artista'),
    path('song/<int:song_id>/', views.detalle_cancion, name='detalle_cancion'),
    # formularios para crear elementos(comentado de momento para que no falle el servidor )
    path('album/form/', views.form_album, name='form_album'),
    path('artist/form/', views.form_artist, name='form_artista'),
    path('song/form/', views.form_song, name='form_cancion'),
    # Editar y eliminar comentarios
    path('comments/delete/<int:comment_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    #path('comments/edit/<int:comment_id>/', views.editar_comentario, name='editar_comentario'),
    
]
