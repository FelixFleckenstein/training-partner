from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from datetime import datetime

from person.models import Person, BodyWeight, BodyFat, BodyDimension

@login_required
def index(request):
	return HttpResponse("Hello, wold. You´re at the Person index.")

@login_required
def addKg(request):
	person = Person.objects.get(id=request.user.id)
	kg = BodyWeight(kg=request.POST.get("kg", ""), date=datetime.strptime(request.POST.get("date", ""), '%d.%m.%Y'), personNr=person)
	kg.save()
	return HttpResponseRedirect('/')

@login_required
def addKFA(request):
	person = Person.objects.get(id=request.user.id)
	kfa = BodyFat(personNr=person, kfa=request.POST.get("kfa", ""), date=datetime.strptime(request.POST.get("date", ""), '%d.%m.%Y'), point1=0, point2=0, point3=0, point4=0, point5=0, point6=0, point7=0)
	kfa.save()
	return HttpResponseRedirect('/')

@login_required
def addMessurements(request):
	person = Person.objects.get(id=request.user.id)
	messurements = BodyDimension(personNr=person, breast=request.POST.get("breast", ""), stomach=request.POST.get("stomach", ""), arm=request.POST.get("arm", ""), upperLeg=request.POST.get("upperLeg", ""), date=datetime.strptime(request.POST.get("date", ""), '%d.%m.%Y'), hip=0, lowerLeg=0)
	messurements.save()
	return HttpResponseRedirect('/')