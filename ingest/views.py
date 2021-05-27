from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse_lazy

from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from .models import Upload, Token
from .forms import IngestForm, TokenManagementForm

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import get_user_tokens
from pprint import pprint


class IngestFileView(FormView):
    template_name = 'ingest/ingest.html'
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
    template_name = 'ingest/ingest.html'
    model = Upload
    form_class = IngestForm
    success_url = '/files/'
    
    def form_invalid(self, instance):
        
        print('\n\nForm was INvalid \n\n')
    
    def form_valid(self, instance):
        
        print('\n\nForm was valid \n\n')
        instance.save()
        return super().form_valid(instance)
    

class FilesView(LoginRequiredMixin, TemplateView):
    
    template_name = "ingest/files_list.html"
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Staff can view all
        if user.is_staff:
            tokens = Token.objects.all()
        else:
            tokens = get_user_tokens(user)
        
        udict = {}
        
        for t in tokens:
            qs = Upload.objects.filter(token=t).order_by('-start_time')
            udict[t.token] = qs
        
        context['udict'] = udict
        
        return context


class TokensView(LoginRequiredMixin, FormView):
    
    template_name = "ingest/tokens_list.html"
    form_class = TokenManagementForm
    success_url = None
    
    def __init__(self):
        
        return super().__init__()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        groups = user.groups.all()
        
        # Staff can view all
        if user.is_staff:
            tokens = Token.objects.all()
        else:
            tokens = get_user_tokens(user)
        
        kwargs['user_tokens'] = tokens
        kwargs['user_groups'] = groups
        return kwargs
    
    def get_context_data(self, *args, **kwargs):
        
        print('got these kwargs', kwargs)
        
        self.context = super().get_context_data(*args, **kwargs)
        
        print('this is now context', self.context)
        
        return self.context
    
    def form_valid(self, instance):
        
        new_tokens = instance.cleaned_data['new_tokens']
        
        print(self.requested_tokens)
        self.get_context_data(debug_p = instance.cleaned_data)
        
        return self.get(self.request)
        
        
    
   
