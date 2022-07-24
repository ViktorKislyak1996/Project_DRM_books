from django.db.models import Count, Case, When
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import *
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import BookSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(
        annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))))
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['price']
    search_fields = ['name', 'author']
    ordering_fields = ['price', 'author']

    def perform_update(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class BookRelationViewSet(UpdateModelMixin, GenericViewSet):
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'book'

    def get_object(self):
        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        # print('created', created)
        return obj


def auth(request):
    return render(request, 'oauth.html')
