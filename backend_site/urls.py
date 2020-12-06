from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index' ),
        path('login/', views.login, name='login' ),
        path('logout/', views.logout, name='logout' ),
        path('add_suspect/', views.add_suspect, name='add_suspect'),
        path('adding/', views.add_suspect_data, name='add_suspect_data'),
        path('user/', views.user, name='user'),
        path('suspect_list/', views.suspect_list, name='suspect_list'),
        path('identify_suspects/', views.identify_suspects, name='identify_suspects'),
        path('updating/', views.update_suspect, name='update_suspect'),
        path('deleting/<int:suspectId>/', views.del_suspect, name='del_suspect'),
        # path('faceRecognization/', views.face_check, name='face_check'),

]