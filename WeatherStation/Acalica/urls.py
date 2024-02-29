"""
URL configuration for Acalica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from Station import views as station
urlpatterns = [
    path('adminlog/', admin.site.urls),
    path('', station.home,name='home'),
    path('all_data/', station.livedatasend,name='live'),
    path('today_temp/', station.today,name='tday'),
    path('graph_data/', station.gdatacal,name='graph'),
    path('value_up/', station.valueup,name='valueup'),
    path('day_update/', station.day_update,name='day_update'),
    path('details/', station.viewmoredetails,name='details'),
    path('devicedata/',station.deviceonlydata,name='device'),
    path('alldevicedata/',station.alldeviceonlydata,name='alldevice'),
    path('admin/',station.admindata,name='admindata'),
    path('login/',station.login,name='login'),
    path('logout/',station.logout,name='logout'),
    path('admin/data/',station.dataview,name='dataview'),
    path('admin_data_out/',station.admin_lastdata,name='admin_lastdata')
    
]
