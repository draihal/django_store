from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from .cart import Cart
from .forms import CartAddProductForm
from shop.models import Product


class CartAddView(generic.CreateView):
    http_method_names = ['post', 'head', 'options', ]

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=self.kwargs.get("product_id"))
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        return HttpResponseRedirect(request.POST.get('next', '/'))


class CartRemoveView(generic.DeleteView):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=self.kwargs.get("product_id"))
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetailView(generic.View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        return render(request, 'cart/detail.html', {'cart': cart})
