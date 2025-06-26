from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serialazers.serialazer import RegisterSerializer
from accounts.serialazers.serialazer import LogoutSerializer
from rest_framework import status



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered'}, status=201)
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


