from django.db import router
from django.urls import path
from rest_framework import routers
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',views.getRoutes),
    path('users/',views.getUser.as_view()),
    path('oursystem/',views.getSystem),
    path('oursystem/<str:pk>/',views.getClass),
]