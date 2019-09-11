from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/', views.signup, name='signup'),
    path('<str:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<str:slug>/', views.product_detail, name='product_detail'),
]
