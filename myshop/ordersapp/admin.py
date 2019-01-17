from django.contrib import admin

from ordersapp.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'created',
        'is_active',
        'status',
    ]

    inlines = [
        OrderItemInline
    ]

admin.site.register(Order, OrderModelAdmin)
admin.site.register(OrderItem)


