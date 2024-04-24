import json
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from users.filters import DynamicSearchFilter
from users.models import InvitedUser, Type, Permission, BannedUser
from authentication.models import User, UserInfo
from users.serializers import TypeSerializer, PermissionSerializer
from authentication.serializers import UserSerializer
from rest_framework.decorators import action
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from activitylog.mixins import ActivityLogMixin

@api_view(['GET'])
def test(request):
    if request.method == 'GET':
        data = {
            'user': str(request.user)
        }
        return Response(data, status=status.HTTP_200_OK)



class TypeViewSet(ActivityLogMixin, viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class UserViewSet(ActivityLogMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()

    serializer_class = UserSerializer
    
    filter_backends = (DynamicSearchFilter,)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'message': 'No users found'}, status=status.HTTP_404_NOT_FOUND)


   
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
      
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    @action(methods=['POST'], detail=True)
    def ban_user(self, request, pk):

        try:
            user = User.objects.get(pk=pk)
            banned_user = BannedUser.objects.create(user=user)
            banned_user.save()
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'message': 'User already banned'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User banned'}, status=status.HTTP_201_CREATED)
    @action(methods=['POST', ], detail=False)
    def invite_user(self, request):
        try:
            email = request.data['email']
            user = User.objects.get(email=email)
            return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create(email=email)
            user.set_unusable_password()
            # if there is user_info with body, get_or_create user_info
            if 'user_info' in request.data:
                user_info = request.data['user_info']
                user_info_instance = UserInfo.objects.create(user=user, **user_info)
                user_info_instance.save()
            
            unique_token = get_random_string(length=32)

            invited_user = InvitedUser.objects.create(user=user, token=unique_token)
            invited_user.save()
            # send email to user with the token
            subject = 'Invitation to join the platform'
            message = f'You have been invited to join the platform. Please use the following link to activate your account: {unique_token} {user.pk}'
            send_mail(subject, message, 'from@yourdomain.com', [email])
            
        return Response({'message': 'User invited'}, status=status.HTTP_201_CREATED)
    @action(methods=['POST'], detail=True)
    def accept_invite(self, request, pk):
        # check if there is an invited user with the given pk
        # then, check if request.token matches the token of the invited user


        # if no password with request, abort
        if 'password' not in request.data:
            return Response({'message': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=pk)
            invited_user = InvitedUser.objects.get(user=user)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except InvitedUser.DoesNotExist:
            return Response({'message': 'Invited user not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if invited_user.token == request.data['token']:
                user = invited_user.user
                user.is_active = True
                # set password
                user.set_password(request.data['password'])
                user.save()
                invited_user.delete()
                return Response({'message': 'User activated'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
class PermissionViewSet(ActivityLogMixin,viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    # get all