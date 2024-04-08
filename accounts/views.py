from .serializers import SignUpSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, status


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {'message': 'Sign up successful!', 'data': serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        response = {'message': 'Sign up failed', 'data': serializer.errors}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)