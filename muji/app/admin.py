from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Subcategory)
admin.site.register(ProductClass)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(PaymentMethod)
admin.site.register(Region)
admin.site.register(Shipment)
admin.site.register(OrderItem)
admin.site.register(Item)