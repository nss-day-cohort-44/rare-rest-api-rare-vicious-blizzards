"""View module for handling requests about games"""
from rareapi.models.comment import Comment
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, RareUser, Tag, PostTag
from django.contrib.auth.models import User
from datetime import date


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

        # today = date.today()
        # current_date = today.strftime("%m/%d/%y")

        ordered_posts = posts.order_by('-publication_date')
        
        # past_posts = []
        # for post in ordered_posts:  
        #     if (ordered_posts.publication_date > current_date): 
        #         return past_posts.append(post)
        # print(past_posts)
        serializer = PostSerializer(
            ordered_posts, many=True, context={'request': request})

        return Response(serializer.data)

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "created_on", "content")

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("label",)

class PostTagSerializer(serializers.ModelSerializer):
    
    tag = TagSerializer(many=False)

    class Meta:
        model = PostTag
        fields = ("id", "tag")
        depth=1

# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ("username", "first_name")
        

class RareUserSerializer(serializers.ModelSerializer):

    class Meta:

        # user = UserSerializer(many=False)
        model = RareUser
        fields = ("id", "bio", "user")
        depth=1

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for Posts

    Arguments:
        serializer type
    """

    tags = PostTagSerializer(many=True)
    comments = CommentSerializer(many=True)
    user = RareUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ("id", "title", "publication_date", "post_image", "content", "approved", "category", "user", "comments", "tags")
        depth=2








