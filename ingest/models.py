from django.db import models

# Create your models here.

class Token(models.Model):
    
    token = models.CharField(max_length=100)
    active = models.BooleanField()

class Upload(models.Model):
    
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    blob = models.FileField()
    start_time = models.DateTimeField(auto_now=True)
