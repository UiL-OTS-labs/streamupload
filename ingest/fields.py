from .models import Token
from django import forms
from django.core.exceptions import ObjectDoesNotExist

class TokenCharField(forms.CharField):
    
    def to_python(self, value):
        choice = False
        try:
            choice = Token.objects.get(token=value)
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                "Invalid token",
                code="invalid_token",
                )
        return choice
