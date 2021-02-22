"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, RareUser

class PostsView(ViewSet):
    """Rare Posts"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        rare_user = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.title = request.data["title"]
        post.publication_date = request.data["publicationDate"]
        post.post_image = request.data["postImage"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.category = request.data["category"]
        post.user = rare_user

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """

        posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True, context={'request': request})

        return Response(serializer.data)
        
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for Posts

    Arguments:
        serializer type
    """

    class Meta:
        model = Post
        fields = ("id", "title", "publication_date", "post_image", "content", "approved", "category", "user")