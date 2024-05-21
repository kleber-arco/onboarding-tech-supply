from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from .models import Post
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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

class SpecificPost(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            return Response({'error': 'post not found'}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class KeycloakGenerateToken(APIView):
    def post(self, request):
        url = 'http://host.docker.internal:8081/realms/myrealm/protocol/openid-connect/token'
        incoming_headers = request.headers
        incoming_data = request.data

        outcoming_headers = {
            'Content-Type': incoming_headers.get('Content-Type', 'application/x-www-form-urlencoded')
        }
        outcoming_data = {
            'grant_type': incoming_data.get('grant_type', 'password'),
            'client_id': incoming_data.get('client_id'),
            'username': incoming_data.get('username'),
            'password': incoming_data.get('password'),
            'client_secret': incoming_data.get('client_secret')
        }

        response = requests.post(url, headers=outcoming_headers, data=outcoming_data)

        if response.status_code == 200:
            return JsonResponse(response.json(), status=200)
        else:
            return JsonResponse(response.json(), status=response.status_code)

@method_decorator(csrf_exempt, name='dispatch')
class KeycloakValidateToken(APIView):
    def post(self, request):
        url = 'http://host.docker.internal:8081/realms/myrealm/protocol/openid-connect/token/introspect'
        incoming_headers = request.headers
        incoming_data = request.data

        outcoming_headers = {
            'Content-Type': incoming_headers.get('Content-Type', 'application/x-www-form-urlencoded')
        }
        outcoming_data = {
            'token': incoming_data.get('token'),
            'client_id': incoming_data.get('client_id'),
            'client_secret': incoming_data.get('client_secret')
        }

        response = requests.post(url, headers=outcoming_headers, data=outcoming_data)

        if response.status_code == 200:
            return JsonResponse(response.json(), status=200)
        else:
            return JsonResponse(response.json(), status=response.status_code)
