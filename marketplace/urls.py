from django.urls import path

from . import views

urlpatterns = [
    path('', views.MarketplaceView.as_view(), name='marketplace'),
    path('<slug:vendor_slug>', views.VendorDetailListView.as_view(), name='vendor_detail'),

    # Add to cart
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    # Decrease cart
    path('decrease-cart/<int:food_id>/', views.decrease_cart, name='decrease_cart')
]