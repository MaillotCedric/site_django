from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    # return HttpResponse("Page dashboard !")
    template = loader.get_template('dashboard_accueil.html')
    return HttpResponse(template.render())
