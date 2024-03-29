from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from posts.serializers import PostSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse


from posts.models import Post


@api_view(['GET', 'POST'])
def list_posts(request: Request):
    posts = Post.objects.all()

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'post created successfully',
                'data': serializer.data
            }
            return JsonResponse(response, status=status.HTTP_201_CREATED)
        response = {
            'message': 'validation error',
            'error': serializer.errors
        }
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        serializer = PostSerializer(posts, many=True)
        response = {
            'data': serializer.data,
            'message': 'fetched posts'
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post)
    response = {
        'message': 'fetch post detail successfully',
        'data': serializer.data
    }
    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    data = JSONParser().parse(request)
    serializer = PostSerializer(post, data=data)
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


@api_view(['DELETE'])
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    post.delete()
    response = {
        'message': 'Post deleted'
    }
    return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
