from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *


class BookSerializer(ModelSerializer):
    like_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author', 'like_count', 'annotated_likes')

    def get_like_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
