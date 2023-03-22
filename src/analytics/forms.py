from django import forms
from workoutplan.models import ExerciseBase

class ChooseExerciseForm(forms.Form):
    exercise = forms.ModelChoiceField(queryset=ExerciseBase.objects.all().order_by('name'), label='Übung')