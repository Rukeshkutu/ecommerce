from rest_framework import serializers
from .models import Account, UserProfile
from django.contrib.auth import authenticate, get_user_model

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    
class AccountSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'profile')


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('email', 'username','password', 'password2', 'first_name', 'last_name', 'phone_number')

        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password must Match')
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = Account.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        User = get_user_model()
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Credentials')
        
        if not user.check_password(data['password']):
            raise serializers.ValidationError('Invalid Credentials')

        if not user.is_active:
            raise serializers.ValidationError('Account Disabled')
        # user = authenticate(email = data['email'], password = data['password'])
        # if not user:
        #     raise serializers.ValidationError('Invalid credentials')

        # if not user.is_active:
        #     raise serializers.ValidationError('Account disabled')
        
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(sefl, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('New password must match.')
        return data

