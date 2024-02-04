"""
URL configuration for WeatherStation project.

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
from Station import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('all_data/', views.livedatasend,name='live'),
    path('today_temp/', views.today,name='tday'),
    path('graph_data/', views.gdatacal,name='graph'),
    path('value_up/', views.valueup,name='valueup'),
    path('day_update/', views.day_update,name='day_update'),
    path('details/', views.viewmoredetails,name='details'),
    path('devicedata/',views.deviceonlydata,name='device')
]
