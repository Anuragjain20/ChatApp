from django.urls import path


from . import views



urlpatterns = [
   path('', views.index, name='index'),
   path('room/<room_name>/', views.room, name='room'), 
   path('dashboard/', views.dashboard, name='dashboard')
]
