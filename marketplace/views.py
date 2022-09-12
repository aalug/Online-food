from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView

from .context_processors import get_cart_counter
from .models import Cart
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
        if self.request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=self.request.user)
        else:
            cart_items = None
        context['cart_items'] = cart_items
        return context


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            # Check if the food item exists
            try:
                food_item = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, food_item=food_item)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': chkCart.quantity,
                                         'cart_amount': get_cart_counter(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, food_item=food_item, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': chkCart.quantity,
                                         'cart_amount': get_cart_counter(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': f'This food does not exist! {food_id}'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            # Check if the food item exists
            try:
                food_item = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, food_item=food_item)
                    if chkCart.quantity > 1:
                        # Decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': chkCart.quantity,
                                         'cart_amount': get_cart_counter(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart'})

            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
