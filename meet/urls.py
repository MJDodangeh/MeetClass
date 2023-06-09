from django.urls import path
from .views import ConfirmMeet,RoomList

urlpatterns = [
      path('confirm/',ConfirmMeet.as_view()),
      path('roomlist/',RoomList.as_view())
]