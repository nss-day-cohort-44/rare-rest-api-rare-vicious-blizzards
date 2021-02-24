"""View module for handling requests about games"""
from rareapi.models.comment import Comment
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, RareUser, Tag, PostTag, Category, category
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

        today = date.today()
        publish_date = today.strftime("%Y-%m-%d")

        print("DATE", publish_date)

        post = Post()
        post.title = request.data["title"]
        post.publication_date = publish_date
        post.post_image_url = request.data["postImage"]
        post.content = request.data["content"]
        post.approved = True
        category = Category.objects.get(pk=request.data["category"])
        post.category = category
        post.user = rare_user

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):

        post = Post.objects.get(pk=pk)

        post.title = request.data["title"]
        post.publication_date = post.publication_date
        post.post_image_url = request.data["postImage"]
        post.content = request.data["content"]
        post.approved = True
        category = Category.objects.get(pk=request.data["category"])
        post.category = category
        post.user = post.user

        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        
        for key in request.data:
            setattr(post, key, request.data[key])

        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post instance
        """

        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """

# ORM MEthod that get all Post objects from the DB

        posts = Post.objects.all()

# Orders posts newest to oldest

        ordered_posts = posts.order_by('-publication_date')

# Run the Post objects throught the serializer to parse wanted properties and to return JS readble code.

        serializer = PostSerializer(
            ordered_posts, many=True, context={'request': request})

        return Response(serializer.data)

# The comment model has "related_name" attribute on the "post" Forriegn Key and this virtual attribute give post access to the comment objects as "comments" in the PostSerializer. The CommentSerializer parses the desired fields from the object.


# RareUserSerializer parses the desired fields from the rareuser objects.

# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ["username"]

class RareUserSerializer(serializers.ModelSerializer):

    class Meta:

        # user = UserSerializer(many=False)

        model = RareUser
        fields = ["id", "bio", "user"]
        depth= 1

class CommentSerializer(serializers.ModelSerializer):

    # author = UserSerializer(many=False)

    class Meta:
        model = Comment
        fields = ("id", "created_on", "content", "author")
        depth = 2



# The TagSerializer parses the desired fields from the tag objects.


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("label",)

# The PostTag model has "related_name" attribute on the "post" Foriegn Key and this virtual attribute give post access to the posttag objects as "tags" in the PostSerializer. The PostTagSerializer parses the desired fields from the objects.


class PostTagSerializer(serializers.ModelSerializer):

    tag = TagSerializer(many=False)

    class Meta:
        model = PostTag
        fields = ("id", "tag")
        depth = 1



<<<<<<< HEAD
    class Meta:

        # user = UserSerializer(many=False)
        model = RareUser
        fields = ("id", "bio", "user")
        depth = 1

# The PostSerializer returns the desired fields for a post response and uses the other serializers to only pull the needed date.
=======
>>>>>>> main


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
        fields = ("id", "title", "publication_date", "post_image_url",
                  "content", "approved", "category", "user", "comments", "tags")
        depth = 2


<<<<<<< HEAD
#     class Meta:
#         model = User
#         fields = ("username", "first_name")
=======






>>>>>>> main
