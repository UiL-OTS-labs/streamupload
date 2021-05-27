from django import forms
from .models import Token, Upload     
from .fields import TokenCharField
from .utils import get_user_tokens
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

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
        
        # Split new tokens input into a token per line
        tokens = self.cleaned_data.get('new_tokens')
        tokens = tokens.strip()
        tokens = [t.strip() for t in tokens.split()]
        self.cleaned_data['new_tokens'] = tokens
        
        self.check_exists(tokens)
        
        # Find all tokens marked for deletion
        keys = [k for k in self.cleaned_data if k[:7] == 'delete_' ]
        keys = [k for k in keys if self.cleaned_data[k]]
        keys = [k[7:] for k in keys ]
        self.cleaned_data['deleted'] = keys
        
        for t in self.cleaned_data['deleted']:
            if not self.check_deletable(t):
                raise ValidationError(
                    'Token "{}" has uploads associated with it.'.format(t), code='has_uploads',
                    )
        
    def check_deletable(self, t):
        
        token = Token.objects.get(token=t)
        
        if token.upload_set.count() != 0:
            return False
        
        return True
    
    def check_exists(self, tokens_list):
        
        for token_name in tokens_list:
            qs = Token.objects.filter(token=token_name)
            if qs.count() != 0:
                raise ValidationError(
                    'Token id {} is already in use.'.format(token_name), code='in_use')
        
        return True
        
        
    
    def get_delete_fields(self):
        
        for f in self.fields:
            print(f)
            if f != 'new_tokens':
                yield self.fields[f]
