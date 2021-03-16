from django import forms
from .models import Token, Upload

class IngestForm(forms.ModelForm):
    
    class Meta:
        model = Upload
        fields = ['blob']
