from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE
    )
    cover = models.ImageField(
        upload_to='albums/',
        blank=True
    )

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    audio_file = models.FileField(
        upload_to='songs/'
    )

    cover_image = models.ImageField(
        upload_to='covers/',
        blank=True
    )

    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(max_length=200)

    songs = models.ManyToManyField(
        Song,
        blank=True
    )

    def __str__(self):
        return self.name