from django.urls import path
from . import views, admin

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello, name='hello'),
]