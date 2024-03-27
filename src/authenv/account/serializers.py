from django.forms import ValidationError
from rest_framework import serializers
from account.models import User
# for email sent
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from account.utils import Util


class UserRegrstrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'date_of_birth',
                  'gender', 'address', 'password', 'password2', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    # validate password and conform password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("pwd and CPWD not match")
        return attrs

    def create(self, validated_data):
        user =  User.objects.create_user(**validated_data)
        self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        link = 'http://127.0.0.1:8000/api/user/verify/'+uid+'/' + token
        body = 'click link to verify email ' + link
        data = {
            'subject': 'verify email',
            'body': body,
            'to_email': user.email
        }
        Util.send_email(data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=128, write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserDataViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'date_of_birth',
                  'gender', 'address', 'password']
        
class AllUserDataViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'date_of_birth',
                  'gender', 'address', 'password']

class UserUpdateDetailsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, write_only=True)
    name = serializers.CharField(max_length=255, write_only=True)
    phone = serializers.CharField(max_length=12, write_only=True)
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.ChoiceField(choices=[(
        'male', 'Male'), ('female', 'Female'), ('other', 'Other')], allow_null=True)
    address = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'date_of_birth',
                  'gender', 'address']

    def validate(self, attrs):
        user = self.context.get('user')
        user.email = attrs.get('email')
        user.name = attrs.get('name')
        user.phone = attrs.get('phone')
        user.date_of_birth = attrs.get('date_of_birth')
        user.gender = attrs.get('gender')
        user.address = attrs.get('address')
        user.save()
        return attrs


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['old_password', 'password', 'password2']

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if not check_password(old_password, user.password):
            raise serializers.ValidationError('in correct old password')
        if old_password == password:
            raise serializers.ValidationError(
                'old password and new password are same')
        if password != password2:
            raise serializers.ValidationError('pwd and cnf pwd does not match')
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://127.0.0.1:8000/api/user/reset/'+uid+'/' + token
            body = 'click link to reset pwd ' + link
            data = {
                'subject': 'reset pwd email',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValueError('you are no register')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError(
                    'pwd and cnf pwd does not match')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'token is not valid or expier')

            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('token is not valid or expier')
