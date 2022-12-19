from django.urls import path
from . import views

urlpatterns = [
	path('new-user', views.createUser, name='index'),
	path('user-profile', views.userProfile, name="userProfile"),
]