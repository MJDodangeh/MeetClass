from django.urls import path
from .views import RegisterUser, ChangePermission
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
      path('register/', RegisterUser.as_view()),
      path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
      path('change-permission/',ChangePermission.as_view())
]