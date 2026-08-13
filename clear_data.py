import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Album, Artist, Song

def clear_music_data():
    print("Deleting old music data...")
    
    # Deleting Albums and Artists
    # Note: Deleting Artists will also cascade and delete associated Albums and Songs
    albums_count = Album.objects.all().count()
    artists_count = Artist.objects.all().count()

    Album.objects.all().delete()
    Artist.objects.all().delete()

    print(f"Removed {albums_count} Albums and {artists_count} Artists.")

if __name__ == '__main__':
    clear_music_data()