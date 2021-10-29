from django.urls import path
from .views import index

app_name='harmonic_ui'

urlpatterns = [
    path('',index,name=''),
    path('room', index,name='room'),
    path('welcome', index,name='welcome')
]
