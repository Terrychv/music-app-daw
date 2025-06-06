from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Rating
from catalog.models import Song, Album
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.

@login_required
def comentarios_usuario(request):
    user = request.user

    album_type = ContentType.objects.get_for_model(Album)
    song_type = ContentType.objects.get_for_model(Song)

    # Obtener todos los comentarios del usuario para álbum o canción con un solo queryset
    comentarios_usuario = Comment.objects.filter(
        user=user
    ).filter(
        Q(content_type=album_type) | Q(content_type=song_type)
    ).order_by('-created_at')

    paginator = Paginator(comentarios_usuario, 5)  # 5 comentarios por página (ajústalo a gusto)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'comentarios_usuario.html', {
        'comentarios_usuario': comentarios_usuario,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user and not request.user.is_admin:
        raise PermissionDenied("You do not have permission to delete this comment.")

    if request.method == 'POST':
        content_object = comment.content_object
        comment.delete()

        if content_object.__class__.__name__.lower() == 'album':
            return redirect('detalle_album', album_id=content_object.id)
        elif content_object.__class__.__name__.lower() == 'song':
            return redirect('detalle_cancion', song_id=content_object.id)

    return redirect('home')
        
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user and not request.user.is_admin:
        raise PermissionDenied("You do not have permission to edit this comment.")

    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content:
            comment.content = new_content
            comment.save()

        content_object = comment.content_object
        if content_object.__class__.__name__.lower() == 'album':
            return redirect('detalle_album', album_id=content_object.id)
        elif content_object.__class__.__name__.lower() == 'song':
            return redirect('detalle_cancion', song_id=content_object.id)

    return redirect('home')

@login_required
def like_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': comment.likes.count()
        })
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def ratings_usuario(request):
    song_type = ContentType.objects.get_for_model(Song)
    album_type = ContentType.objects.get_for_model(Album)

    user_song_ratings = Rating.objects.filter(user=request.user, content_type=song_type)
    user_album_ratings = Rating.objects.filter(user=request.user, content_type=album_type)

    # Empaquetamos los datos como diccionarios para facilitar la plantilla
    song_data = [
        {'object': rating.content_object, 'rating': rating.value}
        for rating in user_song_ratings
        if rating.content_object is not None
    ]

    album_data = [
        {'object': rating.content_object, 'rating': rating.value}
        for rating in user_album_ratings
        if rating.content_object is not None
    ]

    return render(request, 'ratings_usuario.html', {
        'user_song_ratings': song_data,
        'user_album_ratings': album_data,
        'tab': request.GET.get('tab', 'songs'),
    })

@login_required
def rate_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    if request.method == 'POST':
        try:
            rating_value = int(request.POST.get('rating'))
            
        

            # Validar que la puntuación esté entre 1 y 5
            if rating_value < 1 or rating_value > 5:
                return redirect('detalle_album', album_id=album_id)

            content_type = ContentType.objects.get_for_model(Album)

            # Actualizar si ya existe
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                content_type=content_type,
                object_id=album.id,
                defaults={'value': rating_value}
            )

        except (ValueError, TypeError):
            pass  # ignoramos valores inválidos

    return redirect('detalle_album', album_id=album_id)

@login_required
def rate_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    rating_value = int(request.POST.get('rating', 0))

    if 1 <= rating_value <= 5:
        content_type = ContentType.objects.get_for_model(song)
        Rating.objects.update_or_create(
            user=request.user,
            content_type=content_type,
            object_id=song.id,
            defaults={'value': rating_value}
        )

    return redirect('detalle_cancion', song_id=song.id)

@login_required
def likes_usuario(request):
    user = request.user

    album_type = ContentType.objects.get_for_model(Album)
    song_type = ContentType.objects.get_for_model(Song)

    # Comentarios con like del usuario, que estén asociados a álbumes o canciones
    liked_comments = Comment.objects.filter(
        likes=user
    ).filter(
        Q(content_type=album_type) | Q(content_type=song_type)
    ).select_related('user__profile').prefetch_related('likes')

    paginator = Paginator(liked_comments, 5)  # Comentarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'likes_usuario.html', {
        'liked_comments': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })