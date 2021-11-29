
from rest_framework import routers
from songs import views as songViews
from albums import views as albumViews
from artists import views as artistViews
from cluster_lyrics import views as clusterLyricViews
from django.contrib import admin
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'songs',songViews.SongView, basename='songs')
router.register(r'albums', albumViews.AlbumView, basename='albums')
router.register(r'artists',artistViews.ArtistView, basename='artists')
router.register(r'clusters',clusterLyricViews.ClusterView, basename='clusters')
router.register(r'emotions',clusterLyricViews.EmotionView, basename='emotions')


urlpatterns = [
	path('admin/', admin.site.urls),
    path('',include('harmonic_ui.urls')),
    path('spotify/', include('spotify.urls')),
    path('api/', include(router.urls)),
]
