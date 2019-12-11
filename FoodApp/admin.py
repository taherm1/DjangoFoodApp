from django.contrib import admin
from . import models


class AdminProductModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'image')


class AdminCartModel(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'user', 'total_price')


class AdminOrderModel(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'user', 'status', 'date')


admin.site.register(models.Product, AdminProductModel)
admin.site.register(models.Cart, AdminCartModel)
admin.site.register(models.Order, AdminOrderModel)
