from django.contrib import admin

# Register your models here.

from .models import Productheader, Product, Contact, Order, OrderUpdate, Category, Coupon

admin.site.register(Productheader)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(Category)
admin.site.register(Coupon)
