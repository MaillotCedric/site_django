from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('releve/', views.releve, name='releve'),
    path('graph/', views.pagegraph, name='graph')
]
