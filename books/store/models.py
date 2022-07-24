from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              related_name='my_books')
    readers = models.ManyToManyField(User, through='UserBookRelation',
                                     related_name='books')

    def __str__(self):
        return self.name


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Normal'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Awesome')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'Username: {self.user.username} book: {self.book.name}'