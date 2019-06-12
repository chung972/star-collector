from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('stars/', views.stars_index, name='index'),
    path('stars/<int:star_id>/', views.stars_detail, name='detail'),
    path('stars/create/', views.StarCreate.as_view(), name='stars_create'),
    path('stars/<int:pk>/update/', views.StarUpdate.as_view(), name='stars_update'),
    path('stars/<int:pk>/delete/', views.StarDelete.as_view(), name='stars_delete'),
    path('stars/<int:star_id>/add_viewing/', views.add_viewing, name='add_viewing'),
    path('observatories/', views.ObservatoryList.as_view(), name='observatories_index'),
    path('observatories/<int:pk>/', views.ObservatoryDetail.as_view(), name='observatories_detail'),
    path('observatories/create/', views.ObservatoryCreate.as_view(), name='observatories_create'),
    path('observatories/<int:pk>/update/', views.ObservatoryUpdate.as_view(), name='observatories_update'),
    path('observatories/<int:pk>/delete/', views.ObservatoryDelete.as_view(), name='observatories_delete'),
]