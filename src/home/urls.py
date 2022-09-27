from urllib.parse import urlparse
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/<int:id_projet>', views.dashboard, name="dashboard")
]