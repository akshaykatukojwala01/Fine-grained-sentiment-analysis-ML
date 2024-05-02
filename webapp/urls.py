"""Canteen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [ 

    path('', views.home, name="Welcome"),
    path('alogin/', views.alogin, name="alogin"), 
    path('usrreg/', views.usrreg, name="usrreg"),    
    path('signupaction/', views.signupaction, name="signupaction"),
    path('ulogin/', views.ulogin, name="ulogin"),    
    path('uloginaction/', views.uloginaction, name="uloginaction"),
    path('uhome/', views.uhome, name="uhome"),
    
   
    path('adminhome/', views.adminhome, name="adminhome"),
    path('adminloginaction/', views.adminlogindef, name="adminloginactiondef"),
 


    path('ulogout/', views.ulogout, name="ulogout"),
    path('trainingpage/', views.trainingpage, name="trainingpage"),
	path('accuracyview/', views.accuracyview, name="accuracyview"),
    
    path('viewgraphs/', views.viewgraphs, name="viewgraphs"),


    path('cnn/', views.cnn, name="cnn"),
    path('ann/', views.ann, name="ann"),
    path('lstm/', views.lstm, name="lstm"),


    path('search/', views.search, name="search"),
    path('sentiresults/', views.sentiresults, name="sentiresults"),
    path('viewgraph2/', views.viewgraph2, name="viewgraph2"),

]


