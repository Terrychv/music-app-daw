from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Rating
from catalog.models import Song, Album
from django.contrib.auth.decorators import login_required
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
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'POST':
        content_object = comment.content_object
        comment.delete()

        if content_object.__class__.__name__.lower() == 'album':
            return redirect('detalle_album', album_id=content_object.id)
        elif content_object.__class__.__name__.lower() == 'song':
            return redirect('detalle_cancion', song_id=content_object.id)
        
    # Si no es POST, no se debe editar nada
    return redirect('home')
        
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

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
    
    # Si no es POST, no se debe editar nada
    return redirect('home')