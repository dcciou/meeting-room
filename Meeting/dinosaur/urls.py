"""
URL configuration for meeting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,re_path,include
#from schedule.views import CalendarView 
from django.urls import path
from . import views


from.import views

app_name = 'dinosaur'

urlpatterns = [
#    path('calendar/', CalendarView.as_view(), name='calendar'),
    re_path(r'^$', views.list, name='list'),#列出所有會議室
    re_path(r'^(?P<id>[0-9]+)/$', views.appointment, name='appointment'),#列出預約情況
    re_path(r'^logi/$', views.logi, name='logi'),
    re_path(r'^logo/$', views.logo, name='logo'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^(?P<id>[0-9]+)/add/$', views.add, name='add'),
    re_path(r'^(?P<room_id>[0-9]+)/(?P<order_id>[0-9]+)/delete/$', views.delete, name='delete'),
#    path('calendar/', views.calendar_view, name='calendar'),
    path('create_event/', views.create_event, name='create_event'),
    path('compact_calendar/<str:calendar_slug>/', views.compact_calendar, name='compact_calendar'),
    path('calendar_data/', views.calendar_data, name='calendar_data'),
 
]

#TEST
# urlpatterns = [
#     path('',views.index,name='index'),
# ]
# urlpatterns = [
#     path('', views.showtemplate),
# ]

