from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('uregister',views.uregister,name='uregister'),
    path('ulogin',views.ulogin,name='ulogin'),
    path('uhome',views.uhome,name='uhome'),
    path('uprofile',views.uprofile,name='uprofile'),
    path('uedit/<int:id>',views.uedit,name='uedit'),
    path('viewcand',views.viewcand,name='viewcand'),
    path('vote/<int:id>',views.vote,name='vote'),
    path('vote_verify1',views.vote_verify1,name='vote_verify1'),

    path('vote_verify2',views.vote_verify2,name='vote_verify2'),

    path('vote_verify3',views.vote_verify3,name='vote_verify3'),
    path('vote_verify4',views.vote_verify4,name='vote_verify4'),
    path('uwinner',views.uresult,name='uwinner'),





]