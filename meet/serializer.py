from rest_framework import serializers

from .models import Room,ConfirmedMeeting

class ConfirmMeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedMeeting
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class Type1Serializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedMeeting
        fields = ("user","room","start_time","end_time")

    def validate(self, data):
        if data.get("date"):
            raise serializers.ValidationError({"date":"The date of this meeting is specified by the user"})
        return data

class Type2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedMeeting
        fields = ("user","room")

    def validate(self, data):
        errors = {}
        if data.get("date"):
            errors["date"] = "The date of this meeting is specified by the user"
        if data.get("start_time"):
            errors["start_time"] = "The start_time of this meeting is specified by the user"
        if data.get("end_time"):
            errors["end_time"] = "The end_time of this meeting is specified by the user"
        if errors:
            raise serializers.ValidationError(errors)
        return data

class Type3Serializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedMeeting
        fields = ("user","room","date","start_time","end_time")

class Type4Serializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedMeeting
        fields = ("user","room","date")

    def validate(self, data):
        errors = {}
        if data.get("start_time"):
            errors["start_time"] = "The start_time of this meeting is specified by the user"
        if data.get("end_time"):
            errors["end_time"] = "The end_time of this meeting is specified by the user"
        if errors:
            raise serializers.ValidationError(errors)
        return data