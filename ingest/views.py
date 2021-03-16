from django.shortcuts import render
from django.views.generic.edit import FormView
from .models import Upload, Token
from .forms import IngestForm


# Create your views here.

class IngestFileView(FormView):
    template_name = 'ingest.html'
    model = Upload
    form_class = IngestForm
    success_url = '/files/'

class IngestStreamView(FormView):
    template_name = 'ingest.html'
    model = Upload
    form_class = IngestForm
    success_url = '/files/'
    
    
