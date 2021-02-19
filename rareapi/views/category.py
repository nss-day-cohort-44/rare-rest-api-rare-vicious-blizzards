"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

# This will handle all the POST for category


class Category(ViewSet):

    def create(self, request):
        category = Category()

        category.label = request.data['label']

        try:
            category.save()
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        # this will handle request for a single category

    def retrieve(self, request, pk=None):

        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponseServerError(ex)

    # This will handle listing out all categories

    def list(self, request):

        category = Category.objects.all()

        seriliazer = CategorySerializer(
            category, many=True, context={'request': request})
    return Response(serializer.data)

    # This will handle the edit of a category

    def destroy(self, request, pk=None):

        try:
        category = Category.objects.get(pk=pk)
        category.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None)
    category = Category.objects.get(pk=pk)
    category.label = request.data['label']

    category.save()
    return Response({}, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label',)
