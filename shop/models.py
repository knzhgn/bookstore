from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_date = models.DateField()

    def __str__(self):
        return self.title
from django.db import models
from .models import Book  # если ещё нет

class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    books = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ от {self.name} ({self.phone})"
