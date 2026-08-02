from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.id')
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'post']
        read_only_fields = ['user']

class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'body', 'created_at', 'updated_at', 'user', 'comments']
        read_only_fields = ['created_at', 'updated_at', 'user']

    def update(self, instance, validated_data):
        if 'image' in validated_data and validated_data['image'] is None:
            validated_data.pop('image')
        return super().update(instance, validated_data)