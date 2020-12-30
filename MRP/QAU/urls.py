from django.urls import path
from QAU import views


app_name = 'QAU'


urlpatterns = [
    path('qau/', views.checkplan, name='checkplan'),
    path('qau/search', views.checkplanfind, name='checkplanfind'),
    # path('study_daysinfo/<str:studynum>/', views.study_daysinfo, name='study_daysinfo'),
    # path('StudyNum/<str:studynum>/', views.StudyNumReceive, name='StudyNumReceive'),
    
]
