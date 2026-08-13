import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from mutagen.easyid3 import EasyID3
from myapp.models import Song, Artist, Album


def update_artist_images():
    """Matches files in media/artists/ to Artist model instances if present."""
    artists_dir = os.path.join('media', 'artists')
    if not os.path.exists(artists_dir):
        return

    for filename in os.listdir(artists_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            artist_name_clean = os.path.splitext(filename)[0].replace('_', ' ').strip()

            for artist in Artist.objects.all():
                if artist.name.lower() in artist_name_clean.lower() or artist_name_clean.lower() in artist.name.lower():
                    artist.image = f"artists/{filename}"
                    artist.save()
                    print(f"[Artist Image Updated] {artist.name} -> artists/{filename}")


def update_albums():
    """Assigns cover images from media/covers/ or linked songs to Album objects."""
    covers_dir = os.path.join('media', 'covers')
    default_artist, _ = Artist.objects.get_or_create(name='Various Artists')

    for album in Album.objects.all():
        cover_found = None

        # 1. Look for a matching image file in media/covers/
        if os.path.exists(covers_dir):
            for filename in os.listdir(covers_dir):
                if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    clean_filename = os.path.splitext(filename)[0].lower()
                    
                    # Match by album name or song name contained in album
                    if album.name.lower() in clean_filename:
                        cover_found = f"covers/{filename}"
                        break
                    
                    # Check if any song in this album matches the cover filename
                    for song in album.song_set.all():
                        if song.title.lower() in clean_filename or clean_filename in song.title.lower():
                            cover_found = f"covers/{filename}"
                            break
                    if cover_found:
                        break

        # 2. If found in covers folder, update album cover
        if cover_found:
            album.cover = cover_found
            album.save()
            print(f"[Linked Cover from covers/] {album.name} -> {cover_found}")

        # 3. Fallback: Use the cover_image from the first song in this album
        else:
            first_song_with_cover = album.song_set.exclude(cover_image='').exclude(cover_image__isnull=True).first()
            if first_song_with_cover and first_song_with_cover.cover_image:
                album.cover = first_song_with_cover.cover_image.name
                album.save()
                print(f"[Used Song Cover] {album.name} -> {album.cover}")


def import_songs():
    """Imports songs from media/songs/ and links Artists, Covers, and Albums."""
    songs_dir = os.path.join('media', 'songs')

    if not os.path.exists(songs_dir):
        print(f"Directory '{songs_dir}' does not exist!")
        return

    for filename in os.listdir(songs_dir):
        if filename.endswith(('.mp3', '.m4a', '.flac', '.mpeg')):
            file_path = os.path.join(songs_dir, filename)
            song_name_no_ext = os.path.splitext(filename)[0]

            # 1. Extract Title, Artist, & Album using Mutagen
            try:
                tags = EasyID3(file_path)
                artist_name = tags.get('artist', ['Unknown Artist'])[0]
                song_title = tags.get('title', [song_name_no_ext])[0]
                album_name = tags.get('album', [song_title])[0]  # Fallback to song title as album name
            except Exception:
                artist_name = 'Unknown Artist'
                song_title = song_name_no_ext
                album_name = song_title

            # 2. Get or Create Artist
            artist_obj, _ = Artist.objects.get_or_create(name=artist_name)

            # 3. Get or Create Album
            album_obj, _ = Album.objects.get_or_create(
                name=album_name,
                defaults={'artist': artist_obj}
            )
            if not album_obj.artist:
                album_obj.artist = artist_obj
                album_obj.save()

            # 4. Check if a matching cover image exists in media/covers/
            cover_relative_path = None
            for ext in ['.jpg', '.jpeg', '.png', '.webp', '.mp3.jpeg', '.mp3.png']:
                possible_cover = os.path.join('media', 'covers', f"{song_name_no_ext}{ext}")
                if os.path.exists(possible_cover):
                    cover_relative_path = f"covers/{song_name_no_ext}{ext}"
                    break

            # 5. Create or Get Song
            song, created = Song.objects.get_or_create(
                title=song_title,
                defaults={
                    'artist': artist_obj,
                    'album': album_obj,
                    'audio_file': f"songs/{filename}",
                    'cover_image': cover_relative_path
                }
            )

            # 6. Update missing attributes if song exists
            updated = False
            if cover_relative_path and not song.cover_image:
                song.cover_image = cover_relative_path
                updated = True
            if album_obj and not song.album:
                song.album = album_obj
                updated = True

            if updated:
                song.save()

            status = "Created" if created else "Updated/Exists"
            print(f"[{status} Song] {song_title} - {artist_name}")


if __name__ == '__main__':
    print("--- Starting Music & Metadata Import ---")
    
    print("\n1. Importing / Updating Songs...")
    import_songs()

    print("\n2. Updating Album Covers from covers/...")
    update_albums()

    print("\n3. Updating Artist Images...")
    update_artist_images()

    print("\n--- Import Finished Successfully! ---")