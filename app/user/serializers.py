from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users."""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long")
        return value

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and returning it """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        if user:
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Unable to authenticate with provided credentials',
                code='authorization')
