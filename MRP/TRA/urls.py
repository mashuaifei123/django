from django.urls import path
# from studys import views
from TRA import views

app_name = 'TRA'


urlpatterns = [
    path('statalist/', views.statalist, name='statalist'),
    path('traininglist/search', views.traininglist, name='traininglist'),

]