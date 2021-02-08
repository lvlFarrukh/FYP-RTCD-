from django.urls import path
from . import views

urlpatterns = [
        path('check_api', views.check_api, name='check_api' ),
        path('get-report/', views.getAllReport, name='getAllReport' ),
        path('get-report/<int:sid>', views.getReport, name='getReport'),
        path('uploadSuspect/', views.uploadSuspect, name='uploadSuspect'),
        path('upload_anonymously/', views.uploadSuspect_anonymous, name='uploadSuspect_anonymous' ),
        path('creat_user/', views.creat_app_user, name='creat_app_user'),
        path('suspect_track/', views.suspect_track, name='suspect_track'),
        path('auth_user_email/', views.check_username_email, name='check_username_email'),
        path('creat_app_user/', views.creat_app_user, name='creat_app_user'),
]