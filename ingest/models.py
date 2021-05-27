from django.db import models
from django.contrib.auth.models import User, Group
from.utils import UploadFilenameFactory

# Create your models here.

class Token(models.Model):
    
    token = models.CharField(max_length=100,
                             unique=True)
    active = models.BooleanField()
    users = models.ManyToManyField(User,
                                   blank=True)
    groups = models.ManyToManyField(Group,
                                    blank=True)
    
    def __str__(self):
        return self.token

class Upload(models.Model):
    
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    blob = models.FileField(upload_to=UploadFilenameFactory('bindata'))
    start_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return 'Upload started on {} with token {}'.format(
            self.start_time,
            self.token,
            )

# TODO upload_to function, filename based on start_time
