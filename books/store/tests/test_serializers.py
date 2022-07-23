from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_serializer(self):
        book_1 = Book.objects.create(name='Test book 1', price=50.10, author="Author_1")
        book_2 = Book.objects.create(name='Test book 2', price=110.12, author="Author_2")
        serializer_data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '50.10',
                'author': "Author_1"
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '110.12',
                'author': "Author_2"
            },
        ]
        print(serializer_data)
        self.assertEqual(serializer_data, expected_data)