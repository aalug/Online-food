from django.urls import path

from . import views

urlpatterns = [
    path('', views.MarketplaceView.as_view(), name='marketplace'),
    path('<slug:vendor_slug>/', views.VendorDetailListView.as_view(), name='vendor_detail'),

    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease-cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    path('delete-cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),

]