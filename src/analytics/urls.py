from django.urls import path
from . import views

urlpatterns = [
	path('exercise-stats', views.exerciseStats, name='exercise-stats'),
]