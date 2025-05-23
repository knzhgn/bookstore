from django.contrib import admin
from .models import Author, Genre, Store, Book, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Store)