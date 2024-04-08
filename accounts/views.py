from .serializers import SignUpSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate


class SignUpView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = SignUpSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {'message': 'Sign up successful!', 'data': serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        response = {'message': 'Sign up failed', 'data': serializer.errors}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request) -> Response:
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            response = {
                'message': 'Login successful!',
                'token': user.auth_token.key,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'Invalid email or password', 'data': {}}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request) -> Response:
        content = {
            'user': str(request.user),
            'token': str(request.auth),
        }
        return Response(data=content, status=status.HTTP_200_OK)
