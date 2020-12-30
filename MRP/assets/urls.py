from django.urls import path
from assets import views


app_name = 'assets'


urlpatterns = [
    # path('report/', views.report, name='report'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('TSMConfStatus/', views.TSMConfStatus, name='TSMConfStatus'),
    path('TSMConfStatus/search', views.TSMstudysearch, name='TSMstudysearch'),
    path('TSMReceive/', views.TSMReceive, name='TSMReceive'),
    path('StudyNum/<str:studynum>/', views.StudyNumConf, name='StudyNumConf'),
    path('studysearch/ajax_get_study_list', views.ajax_get_study_list, name='ajax_get_study_list'),
    # path('StudyNum/<str:studynum>/', views.StudyNumReceive, name='StudyNumReceive'),
    path('studyinfofull/search', views.studyinfofull, name='studyinfofull'),
    # path('', views.dashboard),
]