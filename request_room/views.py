from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import RequestSerializer


class RequestRoomApi(APIView):
    def post(self,request):
            serializer = RequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data["user"] = request.user
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
