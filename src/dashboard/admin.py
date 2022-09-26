from django.contrib import admin

# Register your models here.

from dashboard.models import Projet, Histo, Threads, Comments

admin.site.register(Projet)
admin.site.register(Histo)
admin.site.register(Threads)
admin.site.register(Comments)