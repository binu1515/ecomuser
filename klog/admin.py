from django.contrib import admin
from .models import Cart, Cartitems, Categrory, Check, Order, OrderItem, product, user
# Register your models here.
admin.site.register(user)
admin.site.register(product)
admin.site.register(Categrory)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Check)