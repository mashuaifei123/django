from django.urls import path
# from studys import views
from TSM import views

app_name = 'TSM'


urlpatterns = [
    path('confstatus/', views.confstatus, name='confstatus'),
    path('confstatus/search', views.confstatusfind, name='confstatusfind'),
    path('inventoryinfo/', views.inventoryinfo, name='inventoryinfo'),
    path('inventoryinfo/search', views.inventoryinfofind, name='inventoryinfofind'),
    # path('study_daysinfo/<str:studynum>/', views.study_daysinfo, name='study_daysinfo'),
    # path('StudyNum/<str:studynum>/', views.StudyNumReceive, name='StudyNumReceive'),
    
]