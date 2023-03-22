from django.urls import path
from . import views

urlpatterns = [
	path('index', views.index, name='index'),
	path('workoutdetails', views.workoutDetails, name='workoutDetails'),
	path('create-workout', views.createWorkout, name='createWorkout'),
	path('edit-workout', views.editWorkout, name='editWorkout'),
	path('exercises', views.exercises, name='exercises'),
	path('add-exercise', views.addExercise, name='add-exercise'),
	path('add-sets', views.addSets, name='add-sets'),
]