from django.shortcuts import render
from .models import Album

def catalogo_albums(request):

    top_albums = sorted(Album.objects.all(), key=lambda a: a.average_rating(), reverse=True)[:4]
    return render(request, 'catalog/catalogo_albums.html', {
        'top_albums': top_albums
    })
