from django.urls import path
from .views import index, index_with_authentication

app_name='harmonic_ui'

urlpatterns = [
    path('',index,name=''),
    path('welcome', index_with_authentication,name='welcome'),
    path('artists', index_with_authentication,name='artists'),
    path('albums', index_with_authentication,name='albums'),
    path('artist/<id>', index_with_authentication, name='artist'),
    path('album/<id>', index_with_authentication, name='album'),
    path('search', index_with_authentication,name='search')    
]
