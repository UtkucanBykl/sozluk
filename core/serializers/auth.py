from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework import serializers


User = get_user_model()

__all__ = ['RegisterSerializer', 'LoginSerializer']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=140)
    password = serializers.CharField(max_length=140)
    email = serializers.EmailField(max_length=140)
    kvkk = serializers.BooleanField()
    confirm_password = serializers.CharField(max_length=140)

    def validate(self, attrs):
        if attrs.get('confirm_password') != attrs.get('password'):
            raise serializers.ValidationError('Passwords does not match')
        return attrs

    def validate_username(self, attr):
        if User.objects.filter(username=attr).exists():
            raise serializers.ValidationError('This username already taken')
        return attr

    def validate_email(self, attr):
        if User.objects.filter(email=attr).exists():
            raise serializers.ValidationError('This email already taken')
        return attr

    def validate_kvkk(self, attr):
        if attr is not True:
            raise serializers.ValidationError('KVKK is have to checked')
        return attr

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            email=validated_data['email']
        )
        return True #Todo UserSerializer ile değişecek


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=140)
    password = serializers.CharField(max_length=140)

    def login(self, attrs):
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
        if user is not None:
            return attrs #Todo UserSerializer ile değişecek
        raise serializers.ValidationError('Username or password incorrect')


