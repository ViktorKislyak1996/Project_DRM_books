from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BookSerializer


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.book_1 = Book.objects.create(name='Test book 1', price=50,
                                          author='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=70,
                                          author='Author 3')
        self.book_3 = Book.objects.create(name='Test book 3 Author 1', price=40,
                                          author='Author 2')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 70})
        serializer_data = BookSerializer([self.book_2], many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BookSerializer([self.book_3, self.book_1, self.book_2], many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


