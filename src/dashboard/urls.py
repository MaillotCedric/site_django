from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id_projet>', views.dashboard, name="dashboard"),
    path('releve/<int:id_projet>', views.releve, name='releve'),
    path('annulation/', views.annulation, name='annulation'),
    path('graph/<int:id_projet>', views.pageGraph, name='graph'),
    path('historique/<int:id_projet>', views.historique, name='historique')
]
