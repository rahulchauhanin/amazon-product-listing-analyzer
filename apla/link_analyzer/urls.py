from django.urls import path
from .views import *

#app_name = 'link_analyzer'
urlpatterns = [
    path('', LinkAnalyzerView.as_view(), name='home'),
    path('about/', about, name='about'),
]
