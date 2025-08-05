from django.urls import path
from . import views

urlpatterns = [
    path('', views.ratio_home, name='ratio_home'),
]
