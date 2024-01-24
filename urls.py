from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('pregister',views.pregister,name='pregister'),
    path('plogin',views.plogin,name='plogin'),
    path('phome',views.phome,name='phome'),
    path('pprofile',views.pprofile,name='pprofile'),
    path('pedit/<int:id>',views.pedit,name='pedit'),
    path('pform',views.pform,name='pform'),
    path('plist',views.plist,name='plist'),
    path('pupdate<int:id>',views.pupdate,name='pupdate'),
    path('addcand',views.addcand,name='addcand'),
    path('winner',views.winner,name='winner'),


    
]