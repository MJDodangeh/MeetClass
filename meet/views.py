import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.manager_permission import IsManager
from request_room.models import RequestRoom
from .models import Room,ConfirmedMeeting
from .serializer import ConfirmMeetSerializer, Type1Serializer, Type2Serializer, Type3Serializer, Type4Serializer, \
    RoomSerializer


class ConfirmMeet(APIView):
    permission_classes = [IsManager]
    def post(self,request):
        data = request.data
        try:
            request_room = RequestRoom.objects.get(id = data.pop("request_id"))
            room = Room.objects.get(id = data.get("room"))
        except:
            return Response({"detail":"this room/request not found"},status=status.HTTP_404_NOT_FOUND)
        data["user"] = request_room.user.id
        if room.capacity > request_room.number:
            if request_room.type == 1:
                serializer = Type1Serializer(data = data)
                serializer.validate(data)
                if serializer.is_valid():
                    serializer.validated_data["date"] = request_room.date
                    return self.check_time_and_save(serializer, request_room)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request_room.type == 2:
                serializer = Type2Serializer(data=data)
                serializer.validate(data)
                if serializer.is_valid():
                    serializer.validated_data["date"] = request_room.date
                    serializer.validated_data["start_time"] = request_room.start_time
                    serializer.validated_data["end_time"] = request_room.end_time
                    return self.check_time_and_save(serializer, request_room)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request_room.type == 3:
                serializer = Type3Serializer(data=data)
                serializer.validate(data)
                if serializer.is_valid():
                    return self.check_time_and_save(serializer, request_room)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request_room.type == 4:
                serializer = Type4Serializer(data=data)
                serializer.validate(data)
                if serializer.is_valid():
                    serializer.validated_data["start_time"] = request_room.start_time
                    serializer.validated_data["end_time"] = request_room.end_time
                    return self.check_time_and_save(serializer, request_room)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"detail": "The capacity of this room is not enough for this meeting"}, status=status.HTTP_400_BAD_REQUEST)

    def check_time_and_save(self,serializer,request_room):
        meet = serializer.validated_data
        meetings = ConfirmedMeeting.objects.all()
        start = meet["start_time"]
        end = meet["end_time"]
        for m in meetings:
            if m.date == meet["date"] and m.room == meet["room"]:
                if (start >= m.start_time and start < m.end_time) or (end > m.start_time and end <= m.end_time):
                    return Response({"detail": "There is another meeting in this room at the selected time. Please select another time"},
                                    status=status.HTTP_400_BAD_REQUEST)
        if request_room.type ==  1 or request_room.type == 3:
            start_ = self.timesum(start)
            end_ = self.timesum(end)
            dur_ = self.timesum(request_room.duration)
            if end_ != dur_ + start_:
                return Response({"datail": "The meet duration does not match the value entered by the user"},status=status.HTTP_400_BAD_REQUEST)
        d = serializer.save()
        request_room.delete()
        confirmmeet = ConfirmMeetSerializer(d).data
        return Response(confirmmeet, status=status.HTTP_201_CREATED)

    def timesum(self,time):
        h, m, s = str(time).split(":")
        return datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

class RoomList(APIView):
    permission_classes = [IsManager]
    def get(self,request):
        room = Room.objects.all()
        serializer = RoomSerializer(room,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
