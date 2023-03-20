from django.db import models
from django.utils import timezone
from datetime import date

class Person(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	lastName = models.CharField(max_length=100)
	birthday = models.DateField()
	height = models.FloatField(default=100)

	def getAge(self):
		today = date.today()
		return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
	
	def getHeight(self):
		return self.height/100

class BodyWeight(models.Model):
	id = models.AutoField(primary_key=True)
	personNr = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='weights')
	date = models.DateField(default=timezone.now)
	kg = models.FloatField()

	def getBMI(self, height):
		return round(self.kg / ((height/100)*(height/100)), 2)

class BodyDimension(models.Model):
	id = models.AutoField(primary_key=True)
	personNr = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='dimensions')
	date = models.DateField(default=timezone.now)
	breast = models.FloatField()
	arm  = models.FloatField()
	stomach = models.FloatField()
	hip = models.FloatField()
	upperLeg = models.FloatField()
	lowerLeg = models.FloatField()

class BodyFat(models.Model):
	id = models.AutoField(primary_key=True)
	personNr = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='fats')
	date = models.DateField(default=timezone.now)
	point1 = models.FloatField()
	point2 = models.FloatField()
	point3 = models.FloatField()
	point4 = models.FloatField()
	point5 = models.FloatField()
	point6 = models.FloatField()
	point7 = models.FloatField()
	kfa = models.FloatField(default=0)

	def getKFA(self, alter):
		#IF kaf is not empty return this
		if self.kfa != None and self.kfa > 0:
			return self.kfa

		#IF point 4 is empty, calculate 3-Point value
		if self.point4 == None or self.point4 == 0:
			s = self.point1 + self.point2 + self.point3
			kd = 1.10938 - (0.0008267*s) + (0.0000016*(s*s)) - 0.0002574*alter
			return (495/kd) - 450

		#ELSE calculate 7-Point value
		return 0
		
def uploadBodyPic(instance, filename):
    return 'bodyImages/%s/%s' % (instance.personNr.id, filename)

class BodyOptic(models.Model):
	id = models.AutoField(primary_key=True)
	personNr = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='optics')
	date = models.DateField(default=timezone.now)
	front = models.ImageField(upload_to=uploadBodyPic, null=True)
	frontFlex = models.ImageField(upload_to=uploadBodyPic, null=True)
	side = models.ImageField(upload_to=uploadBodyPic, null=True)
	sideFlex = models.ImageField(upload_to=uploadBodyPic, null=True)
	back = models.ImageField(upload_to=uploadBodyPic, null=True)
	backFlex = models.ImageField(upload_to=uploadBodyPic, null=True)