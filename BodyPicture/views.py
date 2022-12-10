from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from person.models import Person

# Create your views here.
@login_required
def index(request):
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		print("FormOuptut: ")
		print(form.fields)
		if form.is_valid():
			pic = form.save(commit=False)
			person = Person.objects.get(id=request.user.id)
			pic.personNr = person
			pic.save()

			firstPic = None
			lastPic = None

			if(Person.objects.get(id=request.user.id).optics.count() > 0):
				firstPic = Person.objects.get(id=request.user.id).optics.earliest('date').front
				lastPic = Person.objects.get(id=request.user.id).optics.latest('date').front

			return render(request, 'bodypicture/bodypicture.html', {'form': form, 'firstPic': firstPic, 'lastPic': lastPic})
	else:
		form = ImageForm()
		firstPic = None
		lastPic = None

		if(Person.objects.get(id=request.user.id).optics.count() > 0):
			firstPic = Person.objects.get(id=request.user.id).optics.earliest('date').front
			lastPic = Person.objects.get(id=request.user.id).optics.latest('date').front
	return render(request, 'bodypicture/bodypicture.html', {'form': form, 'firstPic': firstPic, 'lastPic': lastPic})