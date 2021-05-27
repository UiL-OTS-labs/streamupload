from django import forms
from .models import Token, Upload     
from .fields import TokenCharField
from .utils import get_user_tokens
from django.contrib.auth.models import Group

class IngestForm(forms.ModelForm):
    
    token = TokenCharField()
    
    class Meta:
        model = Upload
        fields = ['blob', 'token']
    

        

class TokenManagementForm(forms.Form):
    
    new_tokens = forms.CharField(max_length=1000,
                                 label='Enter your desired tokens here, separated by newlines.',
                                 widget=forms.Textarea,
                                 required=False,)
    
    
    def __init__(self, user_tokens=[], user_groups=[], *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        choices = [(g, g) for g in user_groups]
        
        print('groups received', user_groups)
        
        self.fields['group_for'] = forms.ChoiceField(
            choices=choices,
            required=False,
            )
        
        for t in user_tokens:
            field_name = 'delete_' + str(t)
            self.fields[field_name] = forms.BooleanField(required=False,
                                                         label=t,
                                                         )
        
    
    def clean(self):
        
        tokens = self.cleaned_data.get('new_tokens')
        tokens = tokens.strip()
        tokens = [t.strip() for t in tokens.split()]
        
        self.cleaned_data['new_tokens'] = tokens
    
    def get_delete_fields(self):
        
        for f in self.fields:
            print(f)
            if f != 'new_tokens':
                yield self.fields[f]
