
from re import A

from django.contrib.auth.models import User
from api import serializers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, CourseSerializer
from user.models import UserProfileInfo
from oursystem.models import Course
from rest_framework import status

def getRoutes(request):
    routs=[
        {'GET':'/api/oursystem'},
        {'POST':'/api/oursystem/id'},
        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]
    return Response(routs)

class getUser(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getSystem(request):
    oursystem=Course.objects.all()
    serializer=CourseSerializer(oursystem, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getClass(request):
    classroom=Course.objects.all()
    serializer=CourseSerializer(classroom, many=True)
    return Response(serializer.data)