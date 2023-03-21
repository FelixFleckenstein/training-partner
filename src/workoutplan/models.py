from django.db import models
from django.utils import timezone
from datetime import date
from person.models import Person

class MuscleBase(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    # Example Picture???

    def __str__(self):
        """
        String representation
        """
        return self.name

class EquipmentBase(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    # Example Picture

    def __str__(self):
        return self.name

def uploadExercisePic(filename):
    return 'exerciseImages/%s' % (filename)

class ExerciseBase(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    muscles = models.ManyToManyField(MuscleBase)
    equipments = models.ManyToManyField(EquipmentBase)
    # Example Picture
    picture = models.ImageField(upload_to=uploadExercisePic, null=True)
    # Example Video
    
    def __str__(self):
        return self.name

class Workout(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    personNr = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='workouts')
    description = models.CharField(max_length=1000)

class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    workoutNr = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exerciseBaseNr = models.ForeignKey(ExerciseBase, on_delete=models.CASCADE)

class Set(models.Model):
    id = models.AutoField(primary_key=True)
    exerciseNr = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='sets')
    weight = models.FloatField()
    reps = models.PositiveIntegerField()

class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class TemplateDetail(models.Model):
    id = models.AutoField(primary_key=True)
    templateNr = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='exercises')
    exerciseBaseNr = models.ForeignKey(ExerciseBase, on_delete=models.CASCADE)