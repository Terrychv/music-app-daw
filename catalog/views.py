from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Album,Song, Artist,Genre
from django.db.models import Count
from comments.models import Comment, Rating
from django.contrib.auth.decorators import login_required

def catalogo_albums(request):

    user = request.user if request.user.is_authenticated else None

    # Obtiene todos los álbumes, los ordena por su valoración media (de mayor a menor), y se queda solo con los 4 mejores valorados
    top_albums = sorted(Album.objects.all(), key=lambda a: a.average_rating(), reverse=True)[:4]
    # Apunta a cada canción el número total de comentarios (num_comments),las ordena por ese número descendente, y selecciona las 4 con más comentario
    most_commented_songs = Song.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:4]
    # Filtra los comentarios realizados por el usuario autenticado, los ordena por fecha de creacion descendente y se queda con las 3 mas recientes
    recent_comments = Comment.objects.filter(user=user).order_by('-created_at')[:3]if user else []
    # Igual que el anterio pero con las valoraciones
    recent_ratings = Rating.objects.filter(user=user).order_by('-created_at')[:3]if user else []
    
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

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                user=request.user,
                content=content,
                content_object=album  # Usa GenericForeignKey
            )
            return redirect('detalle_album', album_id=album.id)
    
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

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                user=request.user,
                content=content,
                content_object=song  # Usa GenericForeignKey
            )
            return redirect('detalle_cancion', song_id=song.id)
    
    context = {
        'song': song,
        'related_songs': related_songs,
    }
    return render(request, 'catalog/detalle_cancion.html', context)

@login_required
def eliminar_comentario(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    album_id = comment.content_object.id
    comment.delete()

    if isinstance(comment.content_object, Song):
        return redirect('detalle_cancion', song_id=comment.content_object.id)
    else:
        return redirect('detalle_album', album_id=comment.content_object.id)

    
## Vista para los formularios , hay que revisarlo por si se puede implementar de otra manera o esa es la correcta 
""" def form_album(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist_id = request.POST.get('artist')
        release_date = request.POST.get('release_date')
        description = request.POST.get('description')
        genres_ids = request.POST.getlist('genres')
        cover_image = request.FILES.get('cover_image')

        artist = get_object_or_404(Artist, id=artist_id)
        album = Album.objects.create(
            title=title,
            artist=artist,
            release_date=release_date,
            description=description,
            cover_image=cover_image
        )
        album.genres.set(genres_ids)
        return redirect('catalogo_albums')

    artists = Artist.objects.all()
    genres = Genre.objects.all()
    return render(request, 'forms/form_album.html', {
        'artists': artists,
        'genres': genres
    })

def form_artist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        biography = request.POST.get('biography')
        image = request.FILES.get('image')
        artist = Artist.objects.create(name=name, biography=biography, image=image)
        return redirect('catalogo_albums')

    albums = Album.objects.all()
    songs = Song.objects.all()
    return render(request, 'forms/form_artista.html', {
        'albums': albums,
        'songs': songs
    })

def form_song(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist_id = request.POST.get('artist')
        album_id = request.POST.get('album')
        track_number = request.POST.get('track_number')
        duration = request.POST.get('duration')
        genres_ids = request.POST.getlist('genres')
        cover_image = request.FILES.get('cover_image')

        artist = get_object_or_404(Artist, id=artist_id)
        album = get_object_or_404(Album, id=album_id)

        song = Song.objects.create(
            title=title,
            artist=artist,
            album=album,
            track_number=track_number,
            duration=duration,
            cover_image=cover_image
        )
        song.genres.set(genres_ids)
        return redirect('catalogo_albums')

    artists = Artist.objects.prefetch_related('albums')
    genres = Genre.objects.all()
    return render(request, 'forms/form_cancion.html', {
        'artists': artists,
        'genres': genres
    }) """