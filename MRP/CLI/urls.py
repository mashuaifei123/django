from django.urls import path
from CLI import views
# from studys import views


app_name = 'CLI'


urlpatterns = [
    path('cliinfo/', views.cliinfo, name='cliinfo'),
    path('cliinfo/search', views.cliinfofind, name='cliinfofind'),
    path('clireadinginfo/', views.clireadinginfo, name='clireadinginfo'),
    path('clireadinginfo/search', views.clireadinginfofind, name='clireadinginfofind'),
    path('cliLB_BW/search', views.LB_BW_query, name='cliLB_BW'),
    # path('study_daysinfo/<str:studynum>/', views.study_daysinfo, name='study_daysinfo'),
    # path('StudyNum/<str:studynum>/', views.StudyNumReceive, name='StudyNumReceive'),
]