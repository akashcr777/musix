from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Song, Album, Artist, Playlist

def home(request):
    songs = Song.objects.all()

    return render(request, 'home.html', {
        'songs': songs
    })

def search(request):

    query = request.GET.get('q', '')

    songs = Song.objects.filter(
        Q(title__icontains=query) |
        Q(artist__name__icontains=query)
    )

    return render(request, 'search.html', {
        'songs': songs,
        'query': query
    })

def songs(request):

    songs = Song.objects.all()
    playlists = Playlist.objects.all()

    return render(
        request,
        'songs.html',
        {
            'songs': songs,
            'playlists': playlists
        }
    )
def add_to_playlist(request, song_id):

    song = get_object_or_404(
        Song,
        id=song_id
    )

    if request.method == 'POST':

        playlist_id = request.POST.get('playlist_id')
        new_playlist_name = request.POST.get(
            'new_playlist_name',
            ''
        ).strip()

        # Create a new playlist with the custom name
        if new_playlist_name:

            playlist, created = Playlist.objects.get_or_create(
                name=new_playlist_name
            )

        # Use an existing playlist
        elif playlist_id:

            playlist = get_object_or_404(
                Playlist,
                id=playlist_id
            )

        else:

            return redirect('songs')

        # Add the song to the playlist
        playlist.songs.add(song)

    return redirect('songs')

def albums(request):

    albums = Album.objects.all()

    return render(
        request,
        'albums.html',
        {
            'albums': albums
        }
    )





def playlists(request):

    playlists = Playlist.objects.all()

    return render(
        request,
        'playlists.html',
        {
            'playlists': playlists
        }
    )

def playlist_detail(request, playlist_id):

    playlist = get_object_or_404(
        Playlist,
        id=playlist_id
    )

    songs = playlist.songs.all()

    return render(
        request,
        'playlist_detail.html',
        {
            'playlist': playlist,
            'songs': songs
        }
    )

def remove_from_playlist(request, playlist_id, song_id):

    playlist = get_object_or_404(
        Playlist,
        id=playlist_id
    )

    song = get_object_or_404(
        Song,
        id=song_id
    )

    if request.method == 'POST':
        playlist.songs.remove(song)

    return redirect(
        'playlist_detail',
        playlist_id=playlist.id
    )

def delete_playlist(request, playlist_id):

    playlist = get_object_or_404(
        Playlist,
        id=playlist_id
    )

    if request.method == 'POST':
        playlist.delete()

    return redirect('playlists')