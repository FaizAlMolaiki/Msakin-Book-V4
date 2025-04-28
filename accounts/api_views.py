from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, UserProfileSerializer

@api_view(['POST'])
@csrf_exempt
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'الرجاء إدخال اسم المستخدم وكلمة المرور'},
                      status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'بيانات الدخول غير صحيحة'},
                      status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response(
    {
        'token': token.key,
        'user_id': user.pk,
        'username': user.username
    }
    # {
    #             'user_id': user.id,
    #             'username': user.username,
    #             'email': user.email,
    #             'first_name': user.first_name,
    #             'last_name': user.last_name,
    #             'phone': user.profile.phone if hasattr(user, 'profile') else None,  # إذا كانت لديك حقل هاتف في بروفايل
    #             # 'is_active': user.is_active,
    #             # 'is_staff': user.is_staff,
    #             'token': token.key,  # تضمين التوكن
    #         }
    
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    serializer = UserProfileSerializer(request.user.profile)
    return Response(serializer.data)

@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def update_user_profile(request):
    serializer = UserProfileSerializer(request.user.profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
