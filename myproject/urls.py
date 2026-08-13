"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('songs/', views.songs, name='songs'),
    path('songs/<int:song_id>/add-to-playlist/',views.add_to_playlist,name='add_to_playlist'),
    path('albums/', views.albums, name='albums'),
    path('playlists/',views.playlists,name='playlists'),
    path('playlists/<int:playlist_id>/',views.playlist_detail,name='playlist_detail'),
    path('playlists/<int:playlist_id>/remove/<int:song_id>/',views.remove_from_playlist,name='remove_from_playlist'),
    path('playlists/<int:playlist_id>/delete/',views.delete_playlist,name='delete_playlist'),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)