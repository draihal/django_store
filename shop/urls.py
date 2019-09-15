from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<str:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('<int:id>/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
