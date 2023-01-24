from authentication.api.serializers import SignUpSerializer, LogInSerializer
from django.contrib.auth import authenticate

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User

"""
view for user login
"""
class LogIn(viewsets.ViewSet):

    def create(self, request):
        
        serializer = LogInSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                # generate token
                refresh = RefreshToken.for_user(user)
                data['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                return Response(data, status=status.HTTP_200_OK)

            return Response({'message':'please enter valid email or password'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



"""
view for user registration
"""
class SignUpVS(viewsets.ViewSet):

    def create(self, request):

        serializer = SignUpSerializer(data=request.data)

        data = {}

        # check if username and email are already regestered
        filter_username = User.objects.filter(username=serializer.initial_data['username'])
        filter_email = User.objects.filter(email=serializer.initial_data['email'])

        if filter_username.exists():
            return Response({'error': 'Username already exists!!'}, status=status.HTTP_226_IM_USED)
        
        if filter_email.exists():
            return Response({'error': 'Email already exists!!'}, status=status.HTTP_226_IM_USED)
        
        elif serializer.is_valid():
            
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']

            # check password and confirm password are same
            if password != confirm_password:
                return Response({'error': 'password & confirm password should be same!!'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

            # save user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            data['response'] = "Registration Successfull"
            data['username'] = user.username
            data['email'] = user.email

            # generate token
            refresh = RefreshToken.for_user(user)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_200_OK)
        
        return Response({'message':'Please enter valid data'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)