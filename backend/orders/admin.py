from django.contrib import admin

from .models import (
    Order,
    OrderItem,
    OrderStatusHistory,
    ReturnRequest,
    Refund,
)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatusHistory)
admin.site.register(ReturnRequest)
admin.site.register(Refund)