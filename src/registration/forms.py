from django import forms

class NewUserForm(forms.Form):
	userName = forms.CharField(label="Username", max_length=50)
	firstName = forms.CharField(label="Vorname", max_length=100)
	lastName = forms.CharField(label="Nachname", max_length=100)
	password = forms.CharField(label="Passwort", max_length=500)
	birthday = forms.DateField(label="Geburtsdatum")
	height = forms.FloatField(label="Größe")
	weight = forms.FloatField(label="Gewicht")
	kfa = forms.FloatField(label="KFA")
	breast = forms.FloatField(label="Brust")
	stomach = forms.FloatField(label="Bauch")
	arm = forms.FloatField(label="Biezeps")
	upperLeg = forms.FloatField(label="Oberschenkel")

	def __init__(self, *args, **kwargs):
		super(NewUserForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'