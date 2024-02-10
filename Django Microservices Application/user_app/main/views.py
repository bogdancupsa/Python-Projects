from django.shortcuts import render

from .serializers import CustomAuthTokenSerializer, CustomUserSerializer
from .models import CustomUser

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import json
import jwt
from user_app import settings

# Create your views here.

# class CustomAuthToken(ObtainAuthToken):
#     serializer_class = CustomAuthTokenSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data = request.data,
#                         context = {'request': request})
        
#         serializer.is_valid(raise_exception = True)
        
#         user = serializer.validated_data['user']

#         user.is_staff = user.role == 'admin'
#         user.is_verified = True
#         user.is_active = True
#         user.save()
        
#         token, created = Token.objects.get_or_create(user = user)
#         print('Token Key:', token.key)
#         return Response({'token': token.key, 'user_id': user.id, 'role': user.role})

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    token_var = ""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data,
                        context = {'request': request})
        
        serializer.is_valid(raise_exception = True)
        
        user = serializer.validated_data['user']

        user.is_staff = user.role == 'admin'
        user.is_verified = True
        user.is_active = True
        user.save()
        
        refresh = RefreshToken.for_user(user)
        acc_token = str(refresh.access_token)
        print(          refresh.access_token         )

        token_var = jwt.decode(acc_token, "5ahp8kseKOVB_w", algorithms="HS256")                                  

        print(               token_var              )

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'role': user.role
        })

class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role = 'client')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        print("get_queryset")
        # if self.request.method == 'GET':
        return CustomUser.objects.filter(role='client')
        # return CustomUser.objects.none()

    def perform_create(self, serializer):
        print("perform_create")
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            print('Validation Errors:', e.detail)
            return Response({'error': e.detail}, status=400)

        serializer.save(role='client')

    def post(self, request, *args, **kwargs):
        print("POST request data:", request.data)
        print("POST request headers:", request.headers)
        return super().post(request, *args, **kwargs)

class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role = 'client')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        user_id = instance.id
        instance.delete()
        url = "http://localhost:8012/delete_devices_by_id/" + str(user_id) + "/"
        header = {
            "Content-Type":"application/json",
        }
        payload = {

        }
        result = requests.delete(url, data=json.dumps(payload), headers=header)



