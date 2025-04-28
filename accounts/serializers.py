from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "كلمات المرور غير متطابقة"})
        
        # التحقق من وجود اسم المستخدم
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "اسم المستخدم موجود مسبقاً"})
        
        # التحقق من وجود البريد الإلكتروني
        if 'email' in attrs and User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "البريد الإلكتروني مستخدم مسبقاً"})
            
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        phone = validated_data.pop('phone')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        
        # تحديث رقم الهاتف في الملف الشخصي الذي تم إنشاؤه تلقائياً
        user.profile.phone_number = phone
        user.profile.save()
        
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(source='phone_number')
    avatar = serializers.ImageField(source='profile_picture', required=False)
    bio = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_agent = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'id', 'name', 'email', 'phone', 'avatar', 'bio',
            'address', 'city', 'country', 'is_verified', 'is_agent',
            'created_at', 'updated_at'
        )

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # تحديث بيانات المستخدم
        if 'email' in user_data:
            user.email = user_data['email']
        
        # تحديث الملف الشخصي
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        user.save()
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class GoogleLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()

class AppleLoginSerializer(serializers.Serializer):
    identity_token = serializers.CharField()
    authorization_code = serializers.CharField()
