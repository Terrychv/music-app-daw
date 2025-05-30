from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Album,Song, Artist,Genre
from django.db.models import Count
from comments.models import Comment, Rating
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.http import JsonResponse


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

def top_albums(request):
    sort_option = request.GET.get('sort', 'highest_rated')
    genre_slug = request.GET.get('genre')

    albums = Album.objects.all()

    # Filtrar por género si se selecciona
    if genre_slug:
        albums = albums.filter(genres__slug=genre_slug)

    # Ordenar según la opción seleccionada
    if sort_option == 'highest_rated':
        albums = sorted(albums, key=lambda a: a.average_rating() or 0, reverse=True)
    elif sort_option == 'most_rated':
        albums = sorted(albums, key=lambda a: a.total_ratings or 0, reverse=True)
    elif sort_option == 'newest':
        albums = albums.order_by('-release_date')
    elif sort_option == 'oldest':
        albums = albums.order_by('release_date')

    genres = Genre.objects.all()

    return render(request, 'catalog/top_albums.html', {
        'albums': albums,
        'genres': genres,
    })

def top_canciones(request):
    sort_option = request.GET.get('sort', 'most_commented')
    genre_slug = request.GET.get('genre')

    canciones = Song.objects.all()

    # Filtrar por género si se selecciona
    if genre_slug:
        canciones = canciones.filter(genres__slug=genre_slug)

    # Ordenar según la opción seleccionada
    if sort_option == 'most_commented':
        canciones = canciones.annotate(num_comments=Count('comments')).order_by('-num_comments')
    elif sort_option == 'highest_rated':
        # Para rating medio, si tienes un método average_rating en Song similar a Album
        canciones = sorted(canciones, key=lambda c: c.average_rating() or 0, reverse=True)
    elif sort_option == 'most_rated':
        canciones = sorted(canciones, key=lambda c: c.total_ratings or 0, reverse=True)
    elif sort_option == 'newest':
        canciones = canciones.order_by('-created_at')
    elif sort_option == 'oldest':
        canciones = canciones.order_by('created_at')

    genres = Genre.objects.all()

    return render(request, 'catalog/top_canciones.html', {
        'canciones': canciones,
        'genres': genres,
    })

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



    
## Vista para los formularios , hay que revisarlo por si se puede implementar de otra manera o esa es la correcta
@login_required
def form_album(request):
    user = request.user

    # Si es un usuario normal, no puede acceder a esta vista
    if user.role == 'user':
         return redirect('catalogo_albums')

    # Si es admin, puede ver todos los artistas; si es client, solo los suyos
    if user.is_admin:
        artists = Artist.objects.all()
    elif user.is_client:
        artists = Artist.objects.filter(created_by=user)
    else:
        artists = Artist.objects.none()

    genres = Genre.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        artist_id = request.POST.get('artist')
        release_date = request.POST.get('release_date')
        genres_ids = request.POST.getlist('genres')
        cover_image = request.FILES.get('cover_image')

        # Seguridad: validamos que el artista es accesible por el usuario
        artist = get_object_or_404(artists, id=artist_id)

        album = Album.objects.create(
            title=title,
            artist=artist,
            release_date=release_date,
            cover_image=cover_image
        )

        if genres_ids:
            album.genres.set(genres_ids)

        return redirect('detalle_album', album_id=album.id)

    return render(request, 'forms/form_album.html', {
        'artists': artists,
        'genres': genres}
        )

@login_required
def form_artist(request):

    user = request.user

    if user.role == 'user':
         return redirect('catalogo_albums')

    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('biography')
        image = request.FILES.get('image')

        artist = Artist.objects.create(
            name=name,
            bio=bio,
            image=image,
            created_by=user
        )

        return redirect('detalle_artista', artist_id=artist.id)

    return render(request, 'forms/form_artista.html')

@login_required
def form_song(request):
    user = request.user

    if user.role == 'user':
        return redirect('catalogo_albums')

    # ARTISTAS
    if user.is_admin:
        artists = Artist.objects.all()
    elif user.is_client:
        artists = Artist.objects.filter(created_by=user)
    else:
        artists = Artist.objects.none()

    # ÁLBUMES
    if user.is_admin:
        albums = Album.objects.all()
    elif user.is_client:
        albums = Album.objects.filter(artist__created_by=user)
    else:
        albums = Album.objects.none()

    genres = Genre.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        artist_id = request.POST.get('artist')
        album_id = request.POST.get('album')
        track_number = request.POST.get('track_number')
        duration = request.POST.get('duration')
        audio_file = request.FILES.get('audio_file')
        genre_ids = request.POST.getlist('genres')

        # Validación de artista y álbum según el usuario
        artist = get_object_or_404(artists, id=artist_id)
        album = get_object_or_404(albums, id=album_id)

        # Convertir duración a formato timedelta (MM:SS)
        minutes, seconds = map(int, duration.split(':'))
        duration_td = timedelta(minutes=minutes, seconds=seconds)

        song = Song.objects.create(
            title=title,
            artist=artist,
            album=album,
            duration=duration_td,
            track_number=track_number,
            audio_file=audio_file,
        )

        if genre_ids:
            song.genres.set(genre_ids)

        return redirect('detalle_cancion', song_id=song.id)

    return render(request, 'forms/form_cancion.html', {
        'artists': artists,
        'albums': albums,
        'genres': genres,
    })

# funcion para obtener el siguiente numero de cancion correspondiente al album seleccionado
@login_required
def get_next_track_number(request):
    album_id = request.GET.get('album_id')
    if not album_id:
        return JsonResponse({'error': 'Album ID is required'}, status=400)
    
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        return JsonResponse({'error': 'Album not found'}, status=404)
    
    existing_tracks = album.songs.count()
    next_track = existing_tracks + 1
    return JsonResponse({'next_track_number': next_track})