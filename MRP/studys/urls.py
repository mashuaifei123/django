from django.urls import path
from studys import views


app_name = 'studys'


urlpatterns = [

    path('study_daysinfo/<str:studynum>/', views.study_daysinfo, name='study_daysinfo'),
    path('studydaysview', views.studydaysview, name='studydaysview'),
    path('studysGantt/<str:studynum>/', views.studysGantt, name='studysGantt'),
    path('studysGantt', views.studysGantt, name='studysGantt'),
    path('test', views.get_name, name='test'),
    path('sdmanager/', views.sdmanagerinfo, name='sdmanagerinfo'),
    path('sdmanager/search', views.sdmanagerfind, name='sdmanagerfind'),
    path('studyplan/', views.studyplan, name='studyplan'),
    path('studyplan/search', views.studyplanfind, name='studyplanfind'),
    path('studyplancreate/', views.studyplancreate, name='studyplancreate'),
    
    # path('StudyNum/<str:studynum>/', views.StudyNumReceive, name='StudyNumReceive'),
    
]