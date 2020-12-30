from django.urls import path
from PAT import views
# from studys import views


app_name = 'PAT'


urlpatterns = [
    path('pat/', views.info, name='info'),
    path('pat/search', views.infofind, name='infofind'),
    # path('study_daysinfo/<str:studynum>/', views.study_daysinfo, name='study_daysinfo'),
    # path('StudyNum/<str:studynum>/', views.StudyNumReceive, name='StudyNumReceive'),
    
]