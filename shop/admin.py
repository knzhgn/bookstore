from django.contrib import admin
from .models import Book, Author, Genre, Store, Order  # добавили Order

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Store)
admin.site.register(Order)  # 👈 теперь видно в админке
