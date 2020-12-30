"""CMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from assets import views
from django.conf import settings

admin.site.site_header = "MRP后台管理" 
admin.site.site_title = "欢迎使用|MRP后台管理" 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('assets/', include('assets.urls')),
    path('studys/', include('studys.urls')),
    path('ANA/', include('ANA.urls')),
    path('ARC/', include('ARC.urls')),
    path('CLI/', include('CLI.urls')),
    path('PAT/', include('PAT.urls')),
    path('project/', include('project.urls')),
    path('QAU/', include('QAU.urls')),
    path('SEND/', include('SEND.urls')),
    path('TSM/', include('TSM.urls')),
    path('TRA/', include('TRA.urls')),
    path('animal/', include('animal.urls')),
    path('pristima/', include('pristima.urls')),
    path('', views.IndextoActive),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns