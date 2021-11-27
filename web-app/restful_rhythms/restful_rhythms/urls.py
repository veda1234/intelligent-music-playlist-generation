
from rest_framework import routers
from songs import views as songViews
from albums import views as albumViews
from django.contrib import admin
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'songs',songViews.SongView, basename='songs')
router.register(r'albums', albumViews.AlbumView, basename='albums')

urlpatterns = [
	path('admin/', admin.site.urls),
    path('',include('harmonic_ui.urls')),
    path('spotify/', include('spotify.urls')),
    path('api/', include(router.urls)),
]
