from django.urls import path

from marketplace import views

urlpatterns = [
    path('', views.MarketplaceView.as_view(), name='marketplace'),
    path('<slug:vendor_slug>', views.VendorDetailListView.as_view(), name='vendor_detail'),
]