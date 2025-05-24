from django.shortcuts import render
from .models import Album

def catalogo_albums(request):
    albums = Album.objects.all()
    return render(request, 'catalog/catalogo_albums.html', {
        'albums': albums
    })
