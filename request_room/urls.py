from django.urls import path
from .views import RequestRoomApi , RequestRoomList

urlpatterns = [
      path('request/', RequestRoomApi.as_view()),
      path('requestlist/', RequestRoomList.as_view()),
]