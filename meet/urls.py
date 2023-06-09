from django.urls import path
from .views import ConfirmMeet

urlpatterns = [
      path('confirm/',ConfirmMeet.as_view())
]