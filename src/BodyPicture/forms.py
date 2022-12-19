from django import forms
from person.models import BodyOptic

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = BodyOptic
        fields = ('front',)