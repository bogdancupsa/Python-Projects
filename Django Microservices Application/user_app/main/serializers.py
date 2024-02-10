from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace = False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )

            if not user:
                msg = 'Unable to login with provided credentials'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.role:
                msg = 'User does not have an associated role'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password"'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'role'] 
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['username'] = validated_data['name']
        validated_data['password'] = validated_data['name']

        return CustomUser.objects.create_user(**validated_data)