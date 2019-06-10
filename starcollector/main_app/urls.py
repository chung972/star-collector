from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('stars/', views.stars_index, name='index'),
    path('stars/<int:star_id>/', views.stars_detail, name='detail'),
]