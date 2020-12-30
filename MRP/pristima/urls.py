from django.urls import path
from pristima import views


app_name = 'pristima'


urlpatterns = [

    path('Dosage_BW/search', views.Dosage_BW, name='Dosage_BW'),
    path('ScheduleParameter/search', views.ScheduleParameter, name='ScheduleParameter'),
    # path('StudyNum/<str:studynum>/', views.StudyNumReceive, name='StudyNumReceive'),
    
]