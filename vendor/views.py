from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render

from menu.forms import CategoryForm
from .forms import VendorForm
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from django.template.defaultfilters import slugify


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


class FoodItemsByCategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'login'

    def test_func(self):
        return check_role_vendor(self.request.user)

    template_name = 'vendor/fooditems_by_category.html'
    context_object_name = 'fooditems'

    def get_queryset(self):
        vendor = get_vendor(self.request)
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
        return fooditems

    def get_context_data(self, **kwargs):
        context = super(FoodItemsByCategoryListView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = category
        return context


class AddCategoryFormView(FormView):
    template_name = 'vendor/add_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('menu_builder')

    def form_valid(self, form):
        category_name = form.cleaned_data['category_name']
        category = form.save(commit=False)
        category.vendor = get_vendor(self.request)
        category.slug = slugify(category_name)
        form.save()
        messages.success(self.request, 'Category added successfully!')
        return super().form_valid(form)


class EditCategoryView(SuccessMessageMixin,UpdateView):
    model = Category
    template_name = 'vendor/edit_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('menu_builder')
    success_message = 'Category updated successfully!'


def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')
