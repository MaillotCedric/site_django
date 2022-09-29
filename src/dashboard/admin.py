from django.contrib import admin

# Register your models here.

from dashboard.models import Projet, Histo, Threads, Comments, Statut

admin.site.register(Projet)
admin.site.register(Histo)
admin.site.register(Threads)
admin.site.register(Comments)
admin.site.register(Statut)