import http

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.manager_permission import IsManager
from .serializer import RequestSerializer
from .models import RequestRoom

class RequestRoomApi(APIView):
    def post(self,request):
            serializer = RequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data["user"] = request.user
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestRoomList(APIView):
    permission_classes = [IsManager]
    def get(self,request):
        requests = RequestRoom.objects.all()
        serializer = RequestSerializer(requests,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)