from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from django.contrib import messages
from comments.models import Comment, Rating
from catalog.models import Genre
from django.db.models import Count
from itertools import chain
from collections import Counter
from django.contrib.auth import logout
from django.http import JsonResponse
from operator import attrgetter
import json

def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo_albums')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('catalogo_albums')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})

    return render(request, 'users/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo_albums')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')

        # Validación básica
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'users/signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'email already taken.')
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

    # Conteo de likes 
    likes_count = Comment.objects.filter(likes=user).count()

    # Top géneros por cantidad de puntuaciones o comentarios
    # Obtener géneros desde canciones puntuadas por el usuario
    song_ratings = Rating.objects.filter(user=user, content_type__model='song')
    song_genres = Genre.objects.filter(songs__ratings__in=song_ratings).annotate(count=Count('id'))

    # Obtener géneros desde álbumes puntuados por el usuario
    album_ratings = Rating.objects.filter(user=user, content_type__model='album')
    album_genres = Genre.objects.filter(albums__ratings__in=album_ratings).annotate(count=Count('id'))

    # Combinar y ordenar por popularidad
    all_genres = list(chain(song_genres, album_genres))
    genre_counter = Counter([genre.name for genre in all_genres])
    top_genres = genre_counter.most_common(5)
    # Añadir un atributo auxiliar a cada objeto para identificar su tipo
    for c in comentarios:
        c.tipo = 'comentario'

    for p in puntuaciones:
        p.tipo = 'puntuacion'

    # Combinar y ordenar por fecha
    actividad = sorted(chain(comentarios, puntuaciones), key=attrgetter('created_at'), reverse=True)

    return render(request, 'users/profile.html', {
        'comentarios': comentarios,
        'puntuaciones': puntuaciones,
        'actividad': actividad,
        'likes_count': likes_count,
        'top_genres': top_genres,
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_username(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_username = data.get('username', '').strip()

            if not new_username:
                return JsonResponse({'success': False, 'error': 'Username cannot be empty.'})

            if CustomUser.objects.filter(username=new_username).exclude(id=request.user.id).exists():
                return JsonResponse({'success': False, 'error': 'Username already taken.'})

            request.user.username = new_username
            request.user.save()
            return JsonResponse({'success': True, 'new_username': new_username})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid data.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})