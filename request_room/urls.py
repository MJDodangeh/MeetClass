from django.urls import path
from .views import RequestRoomApi

urlpatterns = [
      path('request/', RequestRoomApi.as_view()),
]