from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voice', views.voice, name='voice'),
    path('emotion', views.emotion, name='emotion'),
    path('detail', views.dailyDetail, name='detail'),

    # 캘린더
    path('calendar', views.CalendarList.as_view()),
    path('calendar/<int:id>', views.CalendarDetail.as_view()),
    path('analyze', views.Analyze.as_view())
]
