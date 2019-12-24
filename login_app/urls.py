from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.indexView, name='indexView'),
    path('login/', views.loginView, name='loginView'),
    path('logout/', views.logoutView , name="logoutView"),
    path('register/', views.registerView, name='registerView'),
    path('verify/', views.verifyView, name='verifyView'),
    path('dashboard/', views.dashboardView, name='dashboardView'),
    path('registeruser/', views.userregistrationView, name='userregistration'),
]
