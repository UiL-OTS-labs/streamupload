from django import forms
from .models import Token, Upload        

class IngestForm(forms.ModelForm):
    
    token = TokenCharField()
    
    class Meta:
        model = Upload
        fields = ['blob', 'token']
    
    
