from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import APIView, permission_classes, api_view
from posts.serializers import PostSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from accounts.serializers import AuthUserPostsSerializer


class PostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        response = {
            'data': serializer.data,
            'message': 'fetched posts'
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            response = {
                'message': 'post created successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'message': 'validation error',
            'error': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        response = {
            'message': 'fetch post detail successfully',
            'data': serializer.data
        }
        return JsonResponse(response, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Updated post detail successfully',
                'data': serializer.data
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
        response = {
            'message': 'validation error',
            'error': serializer.errors
        }
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        response = {
            'message': 'Post deleted'
        }
        return JsonResponse(response, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_posts_for_auth_user(request: Request):
    serializer = AuthUserPostsSerializer(instance=request.user, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)