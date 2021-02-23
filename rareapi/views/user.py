"""View module for handling requests about tags"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.db.models.functions import Lower
from rareapi.models import RareUser

class Users(ViewSet):
    """Level up tags"""

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
            user = RareUser.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to tags resource

        Returns:
            Response -- JSON serialized list of tags
        """
        # Get all tag records from the database
        user = RareUser.objects.all()

        # Orders users alphabetically

        ordered_users = user.order_by(Lower('user'))
        serializer = UserSerializer(
            ordered_users, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments:
        serializer type
    """
    class Meta:
        model = RareUser
        fields = ('user', 'profile_image','created_on','active','bio')
        depth =1



