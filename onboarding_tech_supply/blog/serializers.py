from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'autor', 'created_at']
        extra_kwargs = {'autor': {'required': False}}
