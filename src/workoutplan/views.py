from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.db.models import Max
from django.db.models import Q

from datetime import datetime

from person.models import Person
from workoutplan.models import Workout, Exercise, ExerciseBase, MuscleBase, EquipmentBase, Set, Template
from workoutplan.forms import CreateWorkoutForm, AddExerciseForm, AddExerciseBaseForm, AddSetsForm, TemplateForm

# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_superuser)
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
	editWorkoutForm = CreateWorkoutForm(prefix='edit')
	templates = TemplateForm()

	context = {'createWoForm': createWorkoutForm, 'workouts': workouts, 'templates': templates, 'editWoForm': editWorkoutForm}
	return render(request, 'workoutplan/workoutplan.html', context)

def workoutDetailsReturn(request, woId):
	person = Person.objects.get(id=request.user.id)

	context = {}
	wo = None
	if person.workouts.count() > 0:
		wo = person.workouts.get(id=woId)
	
	exerciseForm = AddExerciseForm()
	setsForm = AddSetsForm()
	exercises = wo.exercises.all()

	for exercise in exercises:
		try:
			exercise.lastMax = Set.objects.select_related('exerciseNr', 'exerciseNr__workoutNr', 'exerciseNr__workoutNr__personNr').filter(~Q(exerciseNr__workoutNr__id=woId), exerciseNr__exerciseBaseNr=exercise.exerciseBaseNr, exerciseNr__workoutNr__personNr__id=request.user.id).order_by('-exerciseNr__workoutNr__date').values('exerciseNr__workoutNr__date').annotate(max_weight=Max('weight')).first()['max_weight']
		except:
			exercise.lastMax = 0

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

	# Template eintragen
	template = Template.objects.get(id=request.POST.get("template", ""))

	for temp in template.exercises.all():
		ex = Exercise(workoutNr=wo, exerciseBaseNr=ExerciseBase.objects.get(id=temp.exerciseBaseNr.id))
		ex.save()

	return workoutDetailsReturn(request, str(wo.id))

@login_required
def editWorkout(request):
	#check if wo id is owned by actual user
	wo = Workout.objects.get(id=request.POST.get("woId", ""))
	if wo.personNr_id != request.user.id:
		print("This Workout is not owned by this user!")
		return HttpResponseRedirect('/workoutplan/index')

	if request.POST.get("action", "") == "save":
		wo.date = datetime.strptime(request.POST.get("edit-date", ""), '%d.%m.%Y')
		wo.description = request.POST.get("edit-description", "")
		wo.save()
	elif request.POST.get("action", "") == "delete":
		wo.delete()

	return HttpResponseRedirect('/workoutplan/index')

@login_required
def addExercise(request):
	ex = Exercise(workoutNr=Workout.objects.get(id=request.session['woId']), exerciseBaseNr=ExerciseBase.objects.get(id=request.POST.get("exercise", "")))
	ex.save()

	return workoutDetailsReturn(request, request.session['woId'])

@login_required
def addSets(request):
	ex = Exercise.objects.get(id=request.POST.get("exId", ""))
	set = Set(exerciseNr=ex, weight=request.POST.get("weight", ""), reps=request.POST.get("reps", ""))
	set.save()

	return workoutDetailsReturn(request, request.session['woId'])