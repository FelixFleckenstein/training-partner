from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from person.models import Person
from datetime import datetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import base64
from io import BytesIO

from person.forms import AddKgForm, AddKFAForm, AddMessurementForm

class Dataset:
	def __init__(self):
		self.labels = []
		self.data = []

@login_required
def index(request):
	person = Person.objects.get(id=request.user.id)

	gewicht = None
	kfa = None
	bmi = None
	
	gewichte = Dataset()
	kfaAll = Dataset()
	bmis = Dataset()
	dimensionsAll = None

	if person.weights.count() > 0:
		gewicht = person.weights.latest('date').kg
		bmi = person.weights.latest('date').getBMI(person.height)

		for entry in person.weights.all().order_by('date'):
			gewichte.labels.append(datetime.strftime(entry.date, '%d.%m'))
			gewichte.data.append(entry.kg)

			bmis.labels.append(datetime.strftime(entry.date, '%d.%m'))
			bmis.data.append(entry.getBMI(person.height))
	
	if person.fats.count() > 0:
		kfa = "%.2f" % person.fats.latest('date').getKFA(person.getAge())

		for entry in person.fats.all().order_by('date'):
			kfaAll.labels.append(datetime.strftime(entry.date, '%d.%m'))
			kfaAll.data.append(entry.getKFA(person.getAge()))

	if person.dimensions.count() > 0:
		personLatest = person.dimensions.latest('date')
		personFirst = person.dimensions.earliest('date')

	kgForm = AddKgForm()
	kgForm.fields['kg'].initial = gewicht

	kfaForm = AddKFAForm()
	kfaForm.fields['kfa'].initial = kfa

	messurementForm = AddMessurementForm()

	#Picture-Test
	img = Image.open('silhouette.png')
	#img = Image.new('RGB', (450, 450))
	I1 = ImageDraw.Draw(img)

	font = ImageFont.truetype("DejaVuSansMono.ttf", 30)

	I1.text((280, 90), str(personLatest.breast), font=font, fill=(0, 0, 0))
	I1.text((280, 160), str(personLatest.arm), font=font, fill=(0, 0, 0))
	I1.text((280, 230), str(personLatest.stomach), font=font, fill=(0, 0, 0))
	I1.text((280, 295), str(personLatest.upperLeg), font=font, fill=(0, 0, 0))

	I1.text((400, 90), "(" + '{0:+}'.format(personLatest.breast - personFirst.breast) + ")", font=font, fill=(0, 0, 0))
	I1.text((400, 160), "(" + '{0:+}'.format(personLatest.arm - personFirst.arm) + ")", font=font, fill=(0, 0, 0))
	I1.text((400, 230), "(" + '{0:+}'.format(personLatest.stomach - personFirst.stomach) + ")", font=font, fill=(0, 0, 0))
	I1.text((400, 295), "(" + '{0:+}'.format(personLatest.upperLeg - personFirst.upperLeg) + ")", font=font, fill=(0, 0, 0))

	buffer = BytesIO()
	img.save(buffer, "PNG")
	#img.save("test.png")
	imgStream = base64.b64encode(buffer.getvalue()).decode()

	context = {'person': person, 'gewicht': gewicht, 'bmi': bmi, 'kfa': kfa, 'dimensions': dimensionsAll, 'gewichte': gewichte, 'kfaAll': kfaAll, 'bmis': bmis, 'kgForm': kgForm, 'kfaForm': kfaForm, 'messurementForm': messurementForm, 'koerper': imgStream}
	return render(request, 'dashboard/dashboard.html', context)
