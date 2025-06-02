from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Rating
from catalog.models import Song, Album
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

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

    return render(request, 'comentarios_usuario.html', {
        'comentarios_usuario': comentarios_usuario,
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