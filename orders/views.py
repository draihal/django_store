from django.shortcuts import render
from django.views import generic

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


class OrderCreateView(generic.CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': OrderCreateForm()}
        return render(request, 'orders/order/create.html', context)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
        return render(request, 'orders/order/create.html', {'form': form})
