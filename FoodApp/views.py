from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from . import forms
from .models import Product, Cart, Order


def home(request):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity:
            product = Product.objects.get(id=request.POST.get('product'))
            cart = Cart.objects.filter(product=product, user=request.user.id)
            if cart.exists():
                # Product present in cart, update quantity
                cart = cart.first()
                cart.quantity += quantity
                cart.save()

            else:
                # Create a new product
                cart = Cart.objects.create(
                    product=product,
                    user=request.user.id,
                    quantity=quantity)
                cart.save()

            if quantity == '1':
                peices_msg = '(1 peice)'
            else:
                peices_msg = f'({quantity} peices)'
            message = f'{product.name} {peices_msg} added to your cart'
            messages.success(request, message)
        else:
            messages.error(request, 'Please enter quantity')

        return HttpResponseRedirect(reverse('home'))
    else:
        product_list = Product.objects.all()
        count = Cart.objects.filter(user=request.user.id).count()
        context = {"product_list": product_list, 'cart_count': count}
        return render(request, 'FoodApp/home.html', context)


def register(request):
    form = forms.SignUpModel()
    context = {'form': form}
    if request.method == 'POST':
        form = forms.SignUpModel(request.POST)
        user = form.save()
        user.set_password(user.password)
        user.save()

        subject = 'Welcome to Food Ordering'
        message = f'Hi, {user.username}! Thank for registering to Food ordering app'
        recipient_list = [user.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        context['form'] = form
        messages.success(request, 'User registered successfully')
    return render(request, 'FoodApp/register.html', context)


def detail(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'FoodApp/detail.html', context)


@login_required
def cart(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'remove':
            Cart.objects.filter(id=request.POST.get('id')).delete()
            return HttpResponseRedirect(reverse('cart'))
        if request.POST.get('action') == 'update':
            item = Cart.objects.get(id=request.POST.get('id'))
            item.quantity = request.POST.get('quantity')
            item.save()
            return HttpResponseRedirect(reverse('cart'))

    cart_list = Cart.objects.filter(user=request.user.id)
    total = 0
    for item in cart_list:
        total += item.total_price()
    context = {'cart_list': cart_list, 'total': total}

    count = Cart.objects.filter(user=request.user.id).count()
    context['cart_count'] = count
    return render(request, 'FoodApp/cart_list.html', context)


@login_required
def checkout(request):
    cart_list = Cart.objects.filter(user=request.user.id)
    for item in cart_list:
        Order.objects.create(user=item.user, quantity=item.quantity,
                             product=item.product)
    Cart.objects.filter(user=request.user.id).delete()

    subject = 'Thank you for your order'
    message = f'Hi, {request.user.username}! Thank for ordering with Food App'
    recipient_list = [request.user.email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    messages.success(request, 'Order placed successfully')

    return render(request, 'FoodApp/cart_list.html')


class OrderHistory(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id).order_by('-date')
