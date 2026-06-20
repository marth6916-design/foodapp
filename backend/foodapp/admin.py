from django.contrib import admin
from .models import Food,Cart,Order,OrderItem,Restaurant,Review

admin.site.register(Food)
admin.site.register(Cart)
admin.site.register(Restaurant)
admin.site.register(Review)