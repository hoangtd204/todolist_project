# accounts/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        token_iat = validated_token.get("iat")
        user_last_pwd_change = user.last_password_change.timestamp()

        if token_iat and token_iat < user_last_pwd_change:
            raise AuthenticationFailed("This token was issued before the password was changed.")

        return user
