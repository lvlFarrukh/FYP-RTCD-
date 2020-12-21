from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index' ),
        path('get-report/', views.getAllReport, name='getAllReport' ),
        path('get-report/<int:sid>', views.getReport, name='getReport'),
        path('uploadSuspect/', views.uploadSuspect, name='uploadSuspect'),
        path('upload_anonymously/', views.uploadSuspect_anonymous, name='uploadSuspect_anonymous' ),
        path('creat_user/', views.creat_app_user, name='creat_app_user'),
]