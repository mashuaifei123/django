from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pic/', views.pic, name='pic'),
    path('hold/', views.hold, name='hold'),
    path('pic1/', views.ask, name='pic1'),
]