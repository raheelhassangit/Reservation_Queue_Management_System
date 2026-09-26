from rest_framework import serializers
from django.contrib.auth import get_user_model
from organizations.models import Organization
from rest_framework.validators import UniqueValidator


User = get_user_model()


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        validated_data["role"] = User.Role.CUSTOMER
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProviderRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True,
    validators=[UniqueValidator(queryset=User.objects.all())],)
    organization_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "organization_name"]

    def create(self, validated_data):
        org_name = validated_data.pop("organization_name")
        validated_data["role"] = User.Role.PROVIDER
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Organization.objects.create(owner=user, name=org_name)
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]    