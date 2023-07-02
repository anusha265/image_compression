from django.urls import path
from . import views

app_name = 'image_compress'

urlpatterns = [
    path('', views.index, name='index'),
    path('compress/', views.compress_images, name='compress'),  # Add this line
    path('result/', views.result, name='result'),
]
