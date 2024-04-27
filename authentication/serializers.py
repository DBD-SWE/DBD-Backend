# from meetup.serializers import InterestSerializer
from .models import User, UserInfo
# from meetup.models import Interest
from rest_framework import serializers
from users.models import BannedUser, InvitedUser


class UserInfoSerializer(serializers.ModelSerializer):
    # interests = InterestSerializer(many=True, read_only=True)
    # interests_data = ListField(child=serializers.DictField(), write_only=True, required=False)

    class Meta:
        model = UserInfo
        fields = ['full_name', 'date_of_birth', 'occupation', 'biography', 'image']

    def create(self, validated_data):
      
        user_info = UserInfo.objects.create(**validated_data)
       
        return user_info

    def update(self, instance, validated_data):
  
        instance = super().update(instance, validated_data)
        print(validated_data)

 
        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_info = UserInfoSerializer(required=False, allow_null=True)
    # Was user banned? If there is UserBanned object with one to one relationship with user, then user is banned
    banned = serializers.SerializerMethodField()
    # Is user being invited? If there is a InvitedUser object with one to one relationship with user, then user is invited
    invited = serializers.SerializerMethodField()



    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'user_info', 'banned', 'invited')

    def create(self, validated_data):
        user_info_data = validated_data.pop('user_info', None)
        user = User.objects.create_user(**validated_data)

        if user_info_data:
            UserInfo.objects.create(user=user, **user_info_data)

        return user
    
    def update(self, instance, validated_data):
        user_info_data = validated_data.pop('user_info', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if user_info_data:
            userinfo, created = UserInfo.objects.get_or_create(user=instance)
            for attr, value in user_info_data.items():
                setattr(userinfo, attr, value)
            userinfo.save()

        return instance
    
    def get_banned(self, instance):
        return BannedUser.objects.filter(user=instance).exists()
    
    def get_invited(self, instance):
        return InvitedUser.objects.filter(user=instance).exists()



