from django.shortcuts import render
from django.urls import reverse
from . import forms
from .models import Product, Cart, Order
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import ListView


def home(request):
    context = dict()
    if request.method == 'POST':

        if request.POST.get('quantity'):
            product = Product.objects.get(id=request.POST.get('product'))
            if Cart.objects.filter(product=product, user=request.user.id).count():
                # Product present in cart, update quantity
                item = Cart.objects.get(product=product, user=request.user.id)
                print(item)
                item.quantity += int(request.POST.get('quantity'))
                item.save()
                if item.quantity == '1':
                    peices_msg = f'({item.quantity} peice)'
                else:
                    peices_msg = f'({item.quantity} peices)'
                context['msg'] = f'{product.name} {peices_msg} added to your cart'
            else:
                cart = Cart.objects.create(
                    product=product,
                    user=request.user.id,
                    quantity=request.POST.get('quantity'))
                cart.save()
                if cart.quantity == '1':
                    peices_msg = f'({cart.quantity} peice)'
                else:
                    peices_msg = f'({cart.quantity} peices)'
                context['msg'] = f'{product.name} {peices_msg} added to your cart'
        else:
            context['error'] = 'Please enter quantity'

    product_list = Product.objects.all()
    count = Cart.objects.filter(user=request.user.id).count()
    context['product_list'] = product_list
    context['cart_count'] = count
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
        context['msg'] = 'User registered successfully'
    return render(request, 'FoodApp/register.html', context)


def detail(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'FoodApp/detail.html', context)


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

    return render(request, 'FoodApp/cart_list.html', {'msg': 'Order placed successfully'})


class OrderHistory(ListView):
    model = Order
