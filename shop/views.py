from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'shop/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'shop/book_detail.html', {'book': book})
from django.shortcuts import render, redirect, get_object_or_404

def add_to_cart(request, pk):
    cart = request.session.get('cart', [])
    if pk not in cart:
        cart.append(pk)
        request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', [])
    books = Book.objects.filter(pk__in=cart)
    return render(request, 'shop/cart.html', {'books': books})

def remove_from_cart(request, pk):
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)
        request.session['cart'] = cart
    return redirect('view_cart')
from django.contrib import messages

from .models import Order

def checkout(request):
    cart = request.session.get('cart', [])
    books = Book.objects.filter(pk__in=cart)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        if name and phone:
            order = Order.objects.create(name=name, phone=phone)
            order.books.set(books)
            order.save()

            request.session['cart'] = []  # очищаем корзину
            return render(request, 'shop/checkout_success.html', {'name': name})
        else:
            messages.error(request, "Пожалуйста, заполните все поля.")

    return render(request, 'shop/checkout.html', {'books': books})


