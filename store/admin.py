from django.contrib import admin

# Register your models here.

from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = (["name"])

admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
#admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)