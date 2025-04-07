# from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import authenticate, logout
from django.conf import settings
from .models import Account, UserProfile
from .serializers import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register (request):
    serializer = RegistrationSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'message':'Registration succesful.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': AccountSerializer(user).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    serializer = LoginSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh= RefreshToken.for_user(user)
        return Response({
            'refresh' : str(refresh),
            'access': str(refresh.access_token),
            'user': AccountSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    print('User: ', request.user)
    print('Auth: ', request.auth)
    # request.auth.delete()
    # logout(request)
    # return Response({'message': 'Successfully Logged Out'})
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        logout(request)
        return Response({'message': 'Successfully Logged Out'})

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def dashboard(request):
#     orders_count = Order.objects.filter(user=request.user, is_or)
#     profile = UserProfile.objects.get(user=request.user)
#     return Response({
#         'orders_count': orders_count,
#         'profile': UserProfileSerializer(profile).data
#     })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    user = request.user
    profile = user.userprofile

    user_serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    profile_serializer = UserProfileSerializer(profile, data=request.data, partial=True)

    if user_serializer.is_valid() and profile_serializer.is_valid():
        user_serializer.save()
        profile_serializer.save()
        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data
        })

    return Response({
        'errors': user_serializer.errors | profile_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        if not requset.user.check_password(serializer.validated_data['current_password']):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message':'Password updated Successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
