from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from datetime import datetime

from person.models import Person
from workoutplan.models import Workout, Exercise, ExerciseBase, MuscleBase, EquipmentBase, Set
from workoutplan.forms import CreateWorkoutForm, AddExerciseForm, AddExerciseBaseForm, AddSetsForm

# Create your views here.
@login_required
def exercises(request):
	exerciseQuery = ExerciseBase.objects.all()
	baseForm = AddExerciseBaseForm()

	if request.method == 'POST':
		form = AddExerciseBaseForm(request.POST)
		if form.is_valid():
			form.save()

	context = {'baseForm': baseForm, 'exercises': exerciseQuery}
	return render(request, 'workoutplan/exercises.html', context)

@login_required
def index(request):
	workouts = []

	person = Person.objects.get(id=request.user.id)

	if person.workouts.count() > 0:
		for entry in person.workouts.all().order_by('-date'):
			workouts.append([entry.date, entry.description, entry.id])

	createWorkoutForm = CreateWorkoutForm()

	context = {'createWoForm': createWorkoutForm, 'workouts': workouts}
	return render(request, 'workoutplan/workoutplan.html', context)

def workoutDetailsReturn(request, woId):
	person = Person.objects.get(id=request.user.id)

	context = {}
	wo = None
	if person.workouts.count() > 0:
		wo = person.workouts.get(id=woId)
	
	exerciseForm = AddExerciseForm()
	setsForm = AddSetsForm()
	exercises = wo.exercises.all


	request.session['woId'] = woId

	context = {'date': wo.date, 'description': wo.description, 'exerciseForm': exerciseForm, 'exercises': exercises, 'setsForm': setsForm}

	return render(request, 'workoutplan/workoutdetails.html', context)

@login_required
def workoutDetails(request):
	return workoutDetailsReturn(request, request.GET.get('id', ''))

@login_required
def createWorkout(request):
	person = Person.objects.get(id=request.user.id)
	wo = Workout(personNr=person, description=request.POST.get("description", ""), date=datetime.strptime(request.POST.get("date", ""), '%d.%m.%Y'))
	wo.save()
	return HttpResponseRedirect('/workoutplan/index')

@login_required
def addExercise(request):
	ex = Exercise(workoutNr=Workout.objects.get(id=request.session['woId']), exerciseBaseNr=ExerciseBase.objects.get(id=request.POST.get("exercise", "")))
	ex.save()

	set = Set(exerciseNr=ex, weight=request.POST.get("weight", ""), reps=request.POST.get("reps", ""))
	set.save()

	return workoutDetailsReturn(request, request.session['woId'])

@login_required
def addSets(request):
	ex = Exercise.objects.get(id=request.POST.get("exId", ""))
	set = Set(exerciseNr=ex, weight=request.POST.get("weight", ""), reps=request.POST.get("reps", ""))
	set.save()

	return workoutDetailsReturn(request, request.session['woId'])