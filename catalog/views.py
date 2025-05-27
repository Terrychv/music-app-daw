from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Album,Song, Artist
from django.db.models import Count
from comments.models import Comment, Rating

def catalogo_albums(request):

    # Obtiene todos los álbumes, los ordena por su valoración media (de mayor a menor), y se queda solo con los 4 mejores valorados
    top_albums = sorted(Album.objects.all(), key=lambda a: a.average_rating(), reverse=True)[:4]
    # Apunta a cada canción el número total de comentarios (num_comments),las ordena por ese número descendente, y selecciona las 4 con más comentario
    most_commented_songs = Song.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:4]
    # Filtra los comentarios realizados por el usuario autenticado, los ordena por fecha de creacion descendente y se queda con las 3 mas recientes
    recent_comments = Comment.objects.filter(user=request.user).order_by('-created_at')[:3]
    # Igual que el anterio pero con las valoraciones
    recent_ratings = Rating.objects.filter(user=request.user).order_by('-created_at')[:3]
    
    return render(request, 'catalog/catalogo_albums.html', {
        'top_albums': top_albums,
        'most_commented_songs': most_commented_songs,
         'recent_comments': recent_comments,
        'recent_ratings': recent_ratings,
    })

def buscar_contenido(request):
    query = request.GET.get('q', '')

    albums = Album.objects.filter(title__icontains=query)
    songs = Song.objects.filter(title__icontains=query)
    artists = Artist.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'albums': albums,
        'songs': songs,
        'artists': artists,
    }

    return render(request, 'catalog/buscar_contenido.html', context)

def detalle_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    comments = album.comments.all().order_by('-created_at')
    
    context = {
        'album': album,
        'comments': comments,
    }
    return render(request, 'catalog/detalle_album.html', context)

def detalle_artista(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    popular_songs = artist.songs.all()[:10]  # Top 10 songs
    
    context = {
        'artist': artist,
        'popular_songs': popular_songs,
    }
    return render(request, 'catalog/detalle_artista.html', context)

def detalle_cancion(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    related_songs = Song.objects.filter(album=song.album).exclude(id=song.id)[:5]
    
    context = {
        'song': song,
        'related_songs': related_songs,
    }
    return render(request, 'catalog/detalle_cancion.html', context)