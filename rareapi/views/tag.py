"""View module for handling requests about tags"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Tag,PostTag

class Tags(ViewSet):
    """Level up tags"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized tag instance
        """
        # Create a new Python instance of the tag class
        # and set its properties from what was sent in the
        # body of the request from the client.
        tag = Tag()
        tag.label = request.data["label"]
        # Try to save the new tag to the database, then
        # serialize the tag instance as JSON, and send the
        # JSON as a response to the client request
        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized tag instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/tags/2
            #
            # The `2` at the end of the route becomes `pk`
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    
    def list(self, request):
        """Handle GET requests to tags resource

        Returns:
            Response -- JSON serialized list of tags
        """
        # Get all tag records from the database
        tags = Tag.objects.all()

        serializer = TagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):
        """Handle PUT requests for a tag

        Returns:
            Response -- Empty body with 204 status code
        """
       # Do mostly the same thing as POST, but instead of
        # creating a new instance of tag, get the tag record
        # from the database whose primary key is `pk`
       tag =Tag.objects.get(pk=pk)
       tag.label = request.data["label"]

       tag.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single tag

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments:
        serializer type
    """
    class Meta:
        model = Tag
        fields = ('id', 'label')
        depth = 1