from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAdminUser

from .models import User
from .serializer import RegisterSerializer


class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": RegisterSerializer(user).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePermission(APIView):
    permission_classes = [IsAdminUser]
    def put(self,request):
        try:
            user = User.objects.get(id = request.data.get("user_id"))
        except:
            return Response({"detail": "any user with this id not found"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_manager = request.data.get("is_manager")
        user.save()
        return Response({"detail": "user " + str(user.id) + " role change to manager"},status=status.HTTP_200_OK)