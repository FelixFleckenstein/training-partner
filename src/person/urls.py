from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('add-kg', views.addKg, name='add-kg'),
	path('add-kfa', views.addKFA, name='add-kfa'),
	path('add-messurements', views.addMessurements, name='add-messurements')
]