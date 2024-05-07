from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import User, UserInfo
from .serializers import UserSerializer, UserInfoSerializer
from django.utils import timezone
from django.contrib.auth import authenticate
from .utils import send_verification_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from rest_framework_simplejwt.views import TokenObtainPairView
from activitylog.mixins import ActivityLogMixin


class CustomTokenObtainPairView(ActivityLogMixin, TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.user
          
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            email = request.data.get('email', None)
            user_login_failed.send(sender=None, request=request, credentials={'email': email})
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterUserView(ActivityLogMixin, APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user)
            return Response({"user": serializer.data,  "message": "Check your email for the verification code."}, status=status.HTTP_201_CREATED)

        # Check if the email is already taken
        if 'email' in serializer.errors:
            return Response({"message": "Email already taken."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Email or password incorrect. Try again later."}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
   
    
    def get(self, request, user_id=None):
      
        # If no user_id is provided, default to the current user's UserInfo
        if user_id is None:
            userinfo = get_object_or_404(UserInfo, user=request.user)
        else:
            # Fetch the UserInfo for the given user_id
            userinfo = get_object_or_404(UserInfo, user__id=user_id)
        serializer = UserInfoSerializer(userinfo)
        return Response({**serializer.data, 'id': userinfo.user.id, 'email': userinfo.user.email})
    def post(self, request):

        user = request.user
        
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=user)
            except IntegrityError:
                return Response({"message": "User info already exists, please use the patch request."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'user_info': serializer.data, 'message': 'successfuly updated user'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request):
        userinfo =  get_object_or_404(UserInfo, user=request.user)  # Ensure it's the user's own UserInfo
        serializer = UserInfoSerializer(userinfo, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email, verification_code=code)
        except User.DoesNotExist:
            return Response({"message": "Invalid email or verification code."}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() - user.code_sent_at <= timezone.timedelta(minutes=30):  # 30 minutes validity
            user.is_active = True
            user.verification_code = None
            user.save()
         


            token_serializer = TokenObtainPairSerializer(data={'email': email, 'password': password
                                                               })

            if token_serializer.is_valid():
                return Response({
                    'access': token_serializer.validated_data.get('access'),
                    'refresh': token_serializer.validated_data.get('refresh'),
                    'message': "Email verified successfully."
                })
            return Response({"ok": "ok"})
        else:
            return Response({"error": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)
