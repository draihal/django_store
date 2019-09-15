from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy

from .models import Category, Product
from cart.forms import CartAddProductForm


class ProductListView(generic.ListView):
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        queryset = Product.objects.filter(available=True)
        if self.kwargs.get("category_slug"):
            category = get_object_or_404(Category, slug=self.kwargs.get("category_slug"))
            queryset = Product.objects.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = None
        categories = Category.objects.all()
        if self.kwargs.get("category_slug"):
            category = get_object_or_404(Category, slug=self.kwargs.get("category_slug"))
        cart_product_form = CartAddProductForm()
        context.update({
            'category': category,
            'categories': categories,
            'cart_product_form': cart_product_form,
        })
        return context


class ProductDetailView(generic.DetailView):
    template_name = 'shop/product/detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Product, id=id_, slug=slug_, available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context.update({
            'cart_product_form': cart_product_form,
        })
        return context


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
