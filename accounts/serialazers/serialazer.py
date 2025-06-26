from rest_framework import serializers
from accounts.models import SimpleUser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        error_messages={
            'unique': 'Username already exists.',
            'blank': 'Username cannot be empty.',
            'required': 'Username is required.'
        }
    )
    class Meta:
        model = SimpleUser
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if SimpleUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value

    def validate(self, attrs):
        if attrs['username'] == attrs['password']:
            raise serializers.ValidationError("Username and password cannot be the same.")
        return attrs

    def create(self, validated_data):
        user = SimpleUser.objects.create_user(**validated_data)
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            self.fail('bad_token')