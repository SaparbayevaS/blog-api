from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from django.contrib.auth import get_user_model
from zoneinfo import available_timezones

User = get_user_model()

class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)
    password2 = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Passwords dont match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
class LanguageSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('language')

class TimezoneSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('timezone',)

    def validate_timezone(self, value):
        if value not in available_timezones():
            raise ValidationError("invalid timezone")
        return value