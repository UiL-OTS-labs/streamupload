"""streamupload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from .views import HomeView
from ingest.views import IngestFileView, IngestStreamView, FilesView, TokensView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ingest/file/', IngestFileView.as_view(), name='ingest'),
    path('ingest/stream/', IngestStreamView.as_view()),
    path('files/', FilesView.as_view(), name='files'),
    path('tokens/', TokensView.as_view(), name='tokens'),
]

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
