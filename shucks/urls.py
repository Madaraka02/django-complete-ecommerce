from django.urls import path

from .views import (
    home, checkoutView, cartView, search, add_to_cart, remove_from_cart, 
    products, details,remove_single_item_from_cart,
    featured, best_seller, catlistView, sendOrderToWhatsapp
)

urlpatterns = [
    path('', home, name='home'),
    path('featured/', featured, name='featured'),
    path('whatsapp/', sendOrderToWhatsapp, name='Whatsapp'),
    path('best-seller/', best_seller, name='best_seller'),
    path('checkout/', checkoutView.as_view(), name='checkout'),
    path('cart/', cartView.as_view(), name='cart'),
    path('search/', search, name='search-results'),
    path('category/<category>', catlistView.as_view(), name='category_products'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('products/', products, name='products'),
    path('details/<int:id>/', details, name='details'),
  
]
