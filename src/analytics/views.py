from django.shortcuts import render
from person.models import Person
from workoutplan.models import Set, ExerciseBase
from analytics.forms import ChooseExerciseForm
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.db.models import Avg

class Dataset:
	def __init__(self):
		self.data1 = []
		self.data2 = []
		self.labels = []

@login_required
def exerciseStats(request):
	person = Person.objects.get(id=request.user.id)

	exId = 1

	if request.method == 'POST':
		exId = request.POST.get("exercise", "")

	exercises = ChooseExerciseForm(initial={'exercise': exId})
	werte = Dataset()

	bankdrueken = Set.objects.select_related('exerciseNr', 'exerciseNr__workoutNr', 'exerciseNr__exerciseBaseNr', 'exerciseNr__workoutNr__personNr') \
		.filter(exerciseNr__exerciseBaseNr__id=exId, exerciseNr__workoutNr__personNr__id=request.user.id) \
		.order_by('exerciseNr__workoutNr__date') \
		.values('exerciseNr__workoutNr__date') \
		.annotate(max_date=Max('exerciseNr__workoutNr__date'), avg_weight=Avg('weight'), avg_reps=Avg('reps')) \
		.order_by()

	for x in bankdrueken:
		print(x)
		werte.data1.append(x["avg_reps"])
		werte.data2.append(x["avg_weight"])
		werte.labels.append(str(x["max_date"]))
		print(x["max_date"])

	context = {'ex': exercises, 'werte': werte}
	return render(request, 'exercise-stats.html', context)