from rest_framework import serializers
from .models import Calendar, Detail, User

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = (
            'calendar_id',
            'user',
            'date',
            'emotion',
        )

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = (
            'detail',
            'sentence',
            'voice',
            'enjoyment',
            'sadness',
            'anger',
            'surprise',
            'disgust',
            'fear',
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'name',
            'age',
            'sex',
            'contact',
            'password',
        )