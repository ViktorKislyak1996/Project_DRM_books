import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BookSerializer


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='testuser1')
        self.book_1 = Book.objects.create(name='Test book 1', price=50,
                                          author='Author 1', owner=self.user1)
        self.book_2 = Book.objects.create(name='Test book 2', price=70,
                                          author='Author 3', owner=self.user1)
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

    def test_create(self):
        url = reverse('book-list')
        data = {
            "name": "Somebook",
            "price": 50,
            "author": "Some Author"}
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(url, json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": "New book name",
            "price": 50,
            "author": "Author 1"}
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.put(url, json_data, content_type='application/json')
        self.book_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.book_1.name, "New book name")
        self.assertEqual(self.user1, Book.objects.first().owner)

    def test_delete(self):
        url = reverse('book-detail', args=(self.book_2.id,))
        previos_list_amount = Book.objects.count()
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        current_list_amount = Book.objects.count()
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(previos_list_amount, current_list_amount + 1)

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='testuser2')
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": "New book name",
            "price": 50,
            "author": "Author 1"}
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, json_data, content_type='application/json')
        self.book_1.refresh_from_db()
        self.assertEqual(response.data, {
            'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                  code='permission_denied')}
                         )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(self.book_1.name, "Test book 1")

    def test_update_not_owner_but_stuff(self):
        self.user2 = User.objects.create(username='testuser2', is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": "New book name",
            "price": 50,
            "author": "Author 1"}
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, json_data, content_type='application/json')
        self.book_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.book_1.name, "New book name")
