from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('sale/', views.sale, name="Sale"),
    path('about/', views.about, name="About"),
    path('contact/', views.contact, name="Contact"),
    path('tracker/', views.tracker, name="Tracker"),
    path('search/', views.search, name="Search"),
    path('products/<int:myid>', views.productview, name="ProductView"),
    path('checkout/', views.checkout, name="Checkout"),
    path('customer_details/', views.customer_details, name="Checkout"),
    path('handlerequest/', views.handlerequest, name="HandleRequest"),
    path('profile/', views.profile, name="Profile"),
]