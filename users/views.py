from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import RegisterSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class RegisterView(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset =  User.objects.all()
    serializer_class = RegisterSerializers
    
    def create(self, request):
        serialized = self.get_serializer(data=request.data)
        # Defining result variable
        result = 'failed'
        data = {"response" : result}
        if serialized.is_valid():

            # Checking for user requirements
            email = request.data['email']
            username = request.data['username']
            password = request.data['password']
            if not len(username) > 150:
                if not len(password) < 8: 
                    try:
                        getUser = User.objects.get(username)
                        print('user')
                        result = 'Username already exist'
                    except Exception as e:
                        try:
                            getUser = User.objects.get(email)
                            print('email')

                            result = 'Email already exist'
                        except Exception as e:
                            try:
                                # Posting user
                                user = User.objects.create_user(
                                    request.data['username'],
                                    request.data['email'],
                                    request.data['password'],
                                )
                                result = 'success'
                                token = Token.objects.get(user=user).key
                                data = {
                                    "response" : result,
                                    "email" : request.data['email'],
                                    "username": request.data['username'],
                                    "token" : token
                                }
                                
                            except Exception as e:
                               pass
                else:
                    result = 'Password is too short'
            else:
                result = 'Username is too short'
        print(request.data)
        return Response(data, status=status.HTTP_201_CREATED)