from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from datetime import datetime

from person.models import Person, BodyWeight, BodyFat, BodyDimension
from .forms import NewUserForm

@login_required
def userProfile(request):
	return render(request, 'registration/user-profile.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def createUser(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			
			#Create Django-User
			user = User.objects.create_user(request.POST.get("userName", ""), '', request.POST.get("password", ""))
			user.first_name = request.POST.get("firstName", "")
			user.last_name = request.POST.get("lastName", "")
			user.save()

			#Create Fitness-User
			person = Person(id=user.id, name=user.first_name, lastName=user.last_name, birthday=datetime.strptime(request.POST.get("birthday", ""), '%d.%m.%Y'), height=request.POST.get("height", ""))
			person.save()

			#Create Weight
			weight = BodyWeight(personNr=person, kg=request.POST.get("weight", ""))
			weight.save()

			#Create KFA
			kfa = BodyFat(personNr=person, kfa=request.POST.get("kfa", ""), point1=0, point2=0, point3=0, point4=0, point5=0, point6=0, point7=0)
			kfa.save()

			#Create BodyDeminsions
			messurements = BodyDimension(personNr=person, breast=request.POST.get("breast", ""), stomach=request.POST.get("stomach", ""), arm=request.POST.get("arm", ""), upperLeg=request.POST.get("upperLeg", ""), hip=0, lowerLeg=0)
			messurements.save()

			return HttpResponseRedirect('/')
		else:
			print(form.errors)
	else:
		form = NewUserForm()
	
	return render(request, 'registration/create-user.html', {'form': form})
