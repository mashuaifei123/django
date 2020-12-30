from django.urls import path
from animal import views
# from studys import views


app_name = 'animal'


urlpatterns = [
    path('animalid/', views.animalid, name='animalid'),
    path('animalid/search', views.animalid, name='animalid'),
    path('F_1F/', views.F_1F, name='F_1F'),
    path('F_2F/', views.F_2F, name='F_2F'),
    path('F_3F/', views.F_3F, name='F_3F'),
    path('F_4F/', views.F_4F, name='F_4F'),

    # path('study_daysinfo/<str:studynum>/', views.study_daysinfo, name='study_daysinfo'),
    # path('StudyNum/<str:studynum>/', views.StudyNumReceive, name='StudyNumReceive'),
    
]