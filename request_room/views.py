import http

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.manager_permission import IsManager
from .serializer import RequestSerializer,RequestWarningSerializer
from .models import RequestRoom,RequestWarning

class RequestRoomApi(APIView):
    def post(self,request):
            serializer = RequestSerializer(data=request.data)
            if serializer.is_valid():
                if serializer.validated_data["type"] == 2:
                    requests = RequestRoom.objects.all()
                    start = serializer.validated_data["start_time"]
                    end = serializer.validated_data["end_time"]
                    date = serializer.validated_data["date"]
                    for req in requests:
                        if req.date == date and req.type == 2:
                            if (start >= req.start_time and start < req.end_time) or (
                                    end > req.start_time and end <= req.end_time):
                                serialize = RequestWarningSerializer(data=request.data)
                                if serialize.is_valid():
                                    serialize.validated_data["user"] = request.user
                                    serialize.save()
                                    return Response({"request_data":serialize.data,
                                                       "Warning": "There is another meeting in this room at the selected time. it be saved?"}, status=status.HTTP_201_CREATED)
                                else:
                                    return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
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

class AcceptWarning(APIView):
    def get(self,request,reqid):
        try:
            req = RequestWarning.objects.get(id = reqid)
        except:
            return Response({"detail": "this request not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user == req.user:
            Req = RequestRoom(number=req.number,date=req.date,start_time=req.start_time,end_time=req.end_time,
                              duration=req.duration,user_id=req.user_id,type=req.type)
            Req.save()
            req.delete()
            return Response({"detail": "warning number " + str(reqid) + " accepted and request created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "This request is not for this user"}, status=status.HTTP_404_NOT_FOUND)
