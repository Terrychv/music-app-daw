from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from django.contrib import messages
from comments.models import Comment, Rating
from catalog.models import Genre
from django.db.models import Count

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Cambia si deseas otra ruta
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})

    return render(request, 'users/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')

        # Validación básica
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'users/signup.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'users/signup.html')

        # Crear el usuario
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Autologin tras crear cuenta
        return redirect('login')

    return render(request, 'users/signup.html')

@login_required
def profile_view(request):
    user = request.user

    comentarios = Comment.objects.filter(user=user).select_related('content_type')
    puntuaciones = Rating.objects.filter(user=user).select_related('content_type')

    # Conteo de likes falsos por ahora (puedes ajustarlo si usas modelo Like)
    likes_count = 312

    # Top géneros por cantidad de puntuaciones o comentarios
    # Obtener géneros desde canciones puntuadas por el usuario
    song_ratings = Rating.objects.filter(user=user, content_type__model='song')
    song_genres = Genre.objects.filter(songs__ratings__in=song_ratings).annotate(count=Count('id'))

    # Obtener géneros desde álbumes puntuados por el usuario
    album_ratings = Rating.objects.filter(user=user, content_type__model='album')
    album_genres = Genre.objects.filter(albums__ratings__in=album_ratings).annotate(count=Count('id'))

    # Combinar y ordenar por popularidad
    from itertools import chain
    from collections import Counter

    all_genres = list(chain(song_genres, album_genres))
    genre_counter = Counter([genre.name for genre in all_genres])
    top_genres = genre_counter.most_common(5)

    return render(request, 'users/profile.html', {
        'comentarios': comentarios,
        'puntuaciones': puntuaciones,
        'likes_count': likes_count,
        'top_genres': top_genres,
    })