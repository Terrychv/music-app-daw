from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation



# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='albums/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='albums', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    comments = GenericRelation('comments.Comment')
    ratings = GenericRelation('comments.Rating')

    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(r.value for r in ratings) / len(ratings)
        return 0


class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    duration = models.DurationField()
    track_number = models.PositiveIntegerField()
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='songs', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    comments = GenericRelation('comments.Comment')
    ratings = GenericRelation('comments.Rating')

    def __str__(self):
        return f"{self.track_number}. {self.title} - {self.artist.name}"

    class Meta:
        ordering = ['track_number']
