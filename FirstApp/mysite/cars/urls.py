from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('showCars', views.showCars, name='showCars'),
    path('timetable', views.timetable, name='timetable'),
]