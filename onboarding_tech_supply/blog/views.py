from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from .models import Post

# Create your views here.

class PostList(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response({'id': post.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        posts = Post.objects.order_by('-created_at')
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)
    
class UpdateAutor(APIView):
    def patch(self, request, post_id):
        new_autor_name = request.data.get('autor')

        try:
            post = Post.objects.get(id=post_id)

            post.autor = new_autor_name
            post.save()

            return Response({'message': 'autor updated successfully'}, status=status.HTTP_200_OK)
        
        except Post.DoesNotExist:
            return Response({'error': 'post not found'}, status=status.HTTP_404_NOT_FOUND)