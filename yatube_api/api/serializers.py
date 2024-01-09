from rest_framework import serializers

from posts.models import Post, Comment, Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username',
                                            read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username',
                                            read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'comments')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
