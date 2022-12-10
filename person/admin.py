from django.contrib import admin
from .models import Person, BodyWeight, BodyFat

admin.site.register(Person)
admin.site.register(BodyWeight)
admin.site.register(BodyFat)