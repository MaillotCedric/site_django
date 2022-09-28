from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dashboard.models import Projet

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home/public.html')
    return render(request, 'home/private.html')

def dashboard(request, id_projet):
    # Si l'utilisateur n'est pas authentifié, ...
    if not request.user.is_authenticated:
        # Je récupère le template de l'accueil publique
        template_accueil_public = loader.get_template('home/public.html')
        
        # L'utilisateur est renvoyé vers la page d'accueil publique
        return HttpResponse(template_accueil_public.render({}, request))
    else:
        # Je récupère le projet à afficher
        projet_a_afficher = Projet.objects.get(codePr=id_projet)

        # Je récupère le template accueil dashboard (dans lequel le projet va être affiché)
        template_accueil_dashboard = loader.get_template('dashboard_accueil.html')

        # Je crée l'objet à injecter dans le template accueil dashboard
        context = {
            'projet': projet_a_afficher
        }

        # L'utilisateur est renvoyé vers la page d'accueil du dashboard (qui contient le projet à afficher)
        return HttpResponse(template_accueil_dashboard.render(context, request))