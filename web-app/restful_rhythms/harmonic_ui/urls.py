from django.urls import path
from .views import index, index_with_authentication

app_name='harmonic_ui'

urlpatterns = [
    path('',index,name=''),
    path('welcome', index_with_authentication,name='welcome')
]
