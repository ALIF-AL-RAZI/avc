from django.db import models
from rest_framework import fields, serializers 
from user.models import UserProfileInfo
from django.contrib.auth.models import User
from oursystem.models import Course, Comment, Reply

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
    
    def create(self, validated_data):
        users=User.objects.all(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password1=validated_data['password1'],
            password2=validated_data['password2'],
            email=validated_data['email'],
            profile_photo=validated_data['email'],
            user_type=validated_data['user_type'],
        )
        return users


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'

class ReplytSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reply
        fields='__all__'