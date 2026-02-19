
from django.contrib import admin
from django.urls import path 

from healthapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    
    path('starter/', views.starter, name='starter'),
    
]
