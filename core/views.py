from django.shortcuts import render
from catalog.models import Album

# Create your views here.

def home(request):
    trending_albums = Album.objects.all()[:6]
    return render(request, 'core/home.html',{'trending_albums': trending_albums})
