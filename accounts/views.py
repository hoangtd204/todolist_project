from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serialazers.serialazer import RegisterSerializer
from accounts.serialazers.serialazer import LogoutSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils import timezone




class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered'}, status=201)
        return Response(serializer.errors, status=400)

class ChangePasswordAndLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        refresh_token = request.data.get('refresh')

        if not old_password or not new_password or not refresh_token:
            return Response({"detail": "Please provide old password, new password, and refresh token."}, status=400)

        if not user.check_password(old_password):
            return Response({"detail": "The old password is incorrect."}, status=400)

        if old_password == new_password:
            return Response({"detail": "The new password must not be the same as the old password."}, status=400)
        user.set_password(new_password)
        user.last_password_change = timezone.now()
        user.save()

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"detail": "Invalid or already blacklisted refresh token."}, status=400)

        return Response({"detail": "Password changed successfully. You have been logged out from all sessions."},
                        status=200)


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Logout successful."}, status=205)
        return Response(serializer.errors, status=400)


