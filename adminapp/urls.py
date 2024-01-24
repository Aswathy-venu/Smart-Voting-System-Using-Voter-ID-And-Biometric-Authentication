from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('alogin',views.alogin,name='alogin'),
    path('aregister',views.aregister,name='aregister'),
    path('index',views.index,name='index'),
    path('tables',views.tables,name='tables'),
    path('result',views.result,name='result'),
    path('start',views.start,name='start'),
    path('end',views.end,name='end'),
    path('approve<int:id>',views.capprove,name='approve'),
    path('reject<int:id>',views.creject,name='reject'),
    path('approveresult<int:id>',views.cresult,name='approveresult'),


    
]