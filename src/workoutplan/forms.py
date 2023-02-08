from django import forms
from datetime import datetime
from workoutplan.models import Exercise, MuscleBase, ExerciseBase

class CreateWorkoutForm(forms.Form):
	date = forms.DateField(label='Datum', initial=datetime.today)
	description = forms.CharField(label='Beschreibung', widget=forms.Textarea())

	def __init__(self, *args, **kwargs):
		super(CreateWorkoutForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class AddExerciseForm(forms.Form):
    exercise = forms.ModelChoiceField(queryset=ExerciseBase.objects.all().order_by('name'), label='Übung')
    weight = forms.IntegerField(required=False, label='Gewicht')
    reps = forms.IntegerField(required=False, label='Reps')

class AddExerciseBaseForm(forms.ModelForm):
	class Meta:
		model = ExerciseBase
		fields = '__all__'

class AddSetsForm(forms.Form):
    exId = forms.IntegerField(required=False, widget=forms.HiddenInput())
    weight = forms.FloatField(required=False, label='Gewicht')
    reps = forms.IntegerField(required=False, label='Reps')