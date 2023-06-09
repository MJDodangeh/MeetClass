from django.urls import path
from .views import RequestRoomApi, RequestRoomList, AcceptWarning

urlpatterns = [
      path('request/room/', RequestRoomApi.as_view()),
      path('requestlist/', RequestRoomList.as_view()),
      path('accept/request/<int:reqid>/', AcceptWarning.as_view()),
]