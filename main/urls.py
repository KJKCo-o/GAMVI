from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voice', views.voice, name='voice'),

    # 캘린더
    path('calendar', views.CalendarList.as_view())
]
