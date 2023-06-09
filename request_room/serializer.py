from rest_framework import serializers

from .models import RequestRoom


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestRoom
        fields = "__all__"
    def validate(self, data):
        if data.get("duration") and (data.get('start_time') or data.get('end_time')):
            raise serializers.ValidationError("please select only one of time or duration")
        elif not data.get("duration") and not (data.get('start_time') or data.get('end_time')):
            raise serializers.ValidationError("please select one of time or duration")
        else:
            if data.get('start_time') and data.get('end_time'):
                if data.get('start_time') > data.get('end_time'):
                    raise serializers.ValidationError("finish must occur after start")
                if data.get('date'):
                    data["type"] = 2
                else:
                    data["type"] = 4
                return data
            else:
                if data.get("duration"):
                    if data.get('date'):
                        data["type"] = 1
                    else:
                        data["type"] = 3
                    return data
                raise serializers.ValidationError("start time and end time must be entered")

