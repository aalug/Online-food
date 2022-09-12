from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from menu.models import FoodItem, Category
from vendor.models import Vendor
from vendor.views import get_vendor


class MarketplaceView(ListView):
    template_name = 'marketplace/listings.html'
    queryset = Vendor.objects.filter(is_approved=True, user__is_active=True)
    context_object_name = 'vendors'

    def get_context_data(self, **kwargs):
        context = super(MarketplaceView, self).get_context_data(**kwargs)
        vendor_count = self.queryset.count()
        context['vendor_count'] = vendor_count
        return context


class VendorDetailListView(ListView):
    """Handles the pages with restaurants menus."""
    template_name = 'marketplace/vendor_detail.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """Fetches categories (from vendor) and then fetches FoodItem objects related to
        those categories - thanks to prefetch_related() and setting related_name in category
        field of FoodItem model"""
        vendor = get_object_or_404(Vendor, vendor_slug=self.kwargs.get('vendor_slug'))
        categories = Category.objects.filter(vendor=vendor).prefetch_related(
            Prefetch(
                'food_items',
                queryset=FoodItem.objects.filter(is_available=True)
            )
        )
        return categories

    def get_context_data(self, **kwargs):
        context = super(VendorDetailListView, self).get_context_data(**kwargs)
        vendor = get_object_or_404(Vendor, vendor_slug=self.kwargs.get('vendor_slug'))
        context['vendor'] = vendor
        return context
