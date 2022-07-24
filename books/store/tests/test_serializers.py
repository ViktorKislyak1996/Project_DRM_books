from django.contrib.auth.models import User
from django.db.models import When, Case, Count
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_serializer(self):
        user1 = User.objects.create(username='testuser1')
        user2 = User.objects.create(username='testuser2')
        user3 = User.objects.create(username='testuser3')
        book_1 = Book.objects.create(name='Test book 1', price=50.10, author="Author_1")
        book_2 = Book.objects.create(name='Test book 2', price=110.12, author="Author_2")
        UserBookRelation.objects.create(user=user1, book=book_1, like=True)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True)
        UserBookRelation.objects.create(user=user1, book=book_2, like=True)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '50.10',
                'author': "Author_1",
                'like_count': 3,
                'annotated_likes': 3
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '110.12',
                'author': "Author_2",
                'like_count': 2,
                'annotated_likes': 2
            },
        ]
        self.assertEqual(serializer_data, expected_data)