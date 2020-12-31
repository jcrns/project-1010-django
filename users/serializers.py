from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')