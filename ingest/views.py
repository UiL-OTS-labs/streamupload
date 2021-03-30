from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from .models import Upload, Token
from .forms import IngestForm

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from pprint import pprint


class IngestFileView(FormView):
    template_name = 'ingest.html'
    model = Upload
    form_class = IngestForm
    success_url = '/files/'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_invalid(self, instance):
        
        print('\n\nForm was INvalid \n\n')
        pprint(instance.cleaned_data)
        pprint(instance.errors)
        return super().form_invalid(instance)
    
    def form_valid(self, instance):
        
        print('\n\nForm was valid \n\n')
        instance.save()
        return super().form_valid(instance)

class IngestStreamView(FormView):
    template_name = 'ingest.html'
    model = Upload
    form_class = IngestForm
    success_url = '/files/'
    
    def form_invalid(self, instance):
        
        print('\n\nForm was INvalid \n\n')
    
    def form_valid(self, instance):
        
        print('\n\nForm was valid \n\n')
        instance.save()
        return super().form_valid(instance)
    

class FilesView(TemplateView):
    
    template_name = "files_list.html"
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        udict = {}    
        tokens = Token.objects.all()
        
        for t in tokens:
            qs = Upload.objects.filter(token=t).order_by('-start_time')
            udict[t.token] = qs
        
        context['udict'] = udict
        
        return context
    
    
