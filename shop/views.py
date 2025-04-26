from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Book, Author, Order
from django.contrib import messages
from django.core.paginator import Paginator

def book_list(request):
    books = Book.objects.all()
    paginator = Paginator(books, 6)  # Показывать по 6 книг на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/book_list.html', {'page_obj': page_obj})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'shop/book_detail.html', {'book': book})

@login_required
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    pk_str = str(pk)
    if pk_str in cart:
        cart[pk_str] += 1
    else:
        cart[pk_str] = 1   
    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})

    if isinstance(cart, list):  # 👈 сбрасываем старую корзину
        cart = {}
        request.session['cart'] = cart

    books = Book.objects.filter(pk__in=cart.keys())
    books_with_quantity = [(book, cart[str(book.pk)]) for book in books]
    return render(request, 'shop/cart.html', {'books_with_quantity': books_with_quantity})


@login_required
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    pk_str = str(pk)
    if pk_str in cart:
        del cart[pk_str]
    request.session['cart'] = cart
    return redirect('view_cart')

from .models import OrderItem  

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    books = Book.objects.filter(pk__in=cart.keys())

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        if name and phone:
            order = Order.objects.create(name=name, phone=phone)
            for book in books:
                OrderItem.objects.create(order=order, book=book, quantity=cart[str(book.pk)])
            request.session['cart'] = []
            return render(request, 'shop/checkout_success.html', {'name': name})
        else:
            messages.error(request, "Пожалуйста, заполните все поля.")
    
    books_with_quantity = [(book, cart[str(book.pk)]) for book in books]
    return render(request, 'shop/checkout.html', {'books_with_quantity': books_with_quantity})
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'shop/profile.html')

def logout_view(request):
    logout(request)
    return redirect('book_list')
def increase_quantity(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 1) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

def decrease_quantity(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        if cart[str(pk)] > 1:
            cart[str(pk)] -= 1
        else:
            del cart[str(pk)]  # если 0 — удалить
    request.session['cart'] = cart
    return redirect('view_cart')