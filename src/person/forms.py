from django import forms
from datetime import datetime

class AddKgForm(forms.Form):
	date = forms.DateField(label='Datum', initial=datetime.today)
	kg = forms.FloatField(label='Gewicht')

	def __init__(self, *args, **kwargs):
		super(AddKgForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class AddKFAForm(forms.Form):
	date = forms.DateField(label='Datum', initial=datetime.today)
	kfa = forms.FloatField(label='KFA')

	def __init__(self, *args, **kwargs):
		super(AddKFAForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class AddMessurementForm(forms.Form):
	date = forms.DateField(label='Datum', initial=datetime.today)
	breast = forms.FloatField(label='Brust')
	stomach = forms.FloatField(label='Bauch')
	arm = forms.FloatField(label='Biezeps')
	upperLeg = forms.FloatField(label='Oberschenkel')

	def __init__(self, *args, **kwargs):
		super(AddMessurementForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'