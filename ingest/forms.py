from django import forms
from .models import Token, Upload     
from .fields import TokenCharField

class IngestForm(forms.ModelForm):
    
    token = TokenCharField()
    
    class Meta:
        model = Upload
        fields = ['blob', 'token']
    
    
