from django.contrib import admin
from .models import *

# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'best_seller']
    list_editable = ['best_seller']      
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category)
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_display = ['title', 'new_price', 'old_price', 'featured', 'brand', 'category']
    list_editable = ['new_price', 'old_price', 'featured', 'brand', 'category']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered_date','get_items']    
admin.site.register(Item, ItemAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'county', 
        'location',
        'phone_number',
        'default'
        ]    
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
