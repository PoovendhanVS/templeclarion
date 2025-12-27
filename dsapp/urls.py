"""" App URL """
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login,name='login'),
    path('login/', views.login,name='login'),
    path('home/', views.home,name='home'),
    path('forgetpwd/', views.forgetpwd,name='forgetpwd'),
    path('register/', views.register,name='register'),
    path('mainmaster/', views.mainmaster,name='mainmaster'),
    path('master/', views.master,name='master'),
    path('userentry/', views.userentry,name='userentry'),
    path('payreport/', views.payreport,name='payreport'),
    # path('requestcredential/', views.requestcredential,name='requestcredential'),
    # path('transalate/', views.transalate,name='transalate'),
    


    path('design/', views.createscreen,name='design'),
    path('designview/', views.show_design,name='designview'),
    path('dashboard/', views.sysdashboard,name='sysdashboard'),
    path('billing/', views.billing,name='billing')
]



