from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, DeleteView, CreateView
from django.shortcuts import get_object_or_404, redirect, render

from menu.forms import CategoryForm, FoodItemForm
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


class AddCategoryFormView(LoginRequiredMixin, UserPassesTestMixin, FormView):

    def test_func(self):
        return check_role_vendor(self.request.user)

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


class EditCategoryView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):

    def test_func(self):
        return check_role_vendor(self.request.user)

    model = Category
    template_name = 'vendor/edit_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('menu_builder')
    success_message = 'Category updated successfully!'


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')


class AddFoodView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return check_role_vendor(self.request.user)

    def get(self, request):
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
        context = {
            'form': form
        }
        return render(request, 'vendor/add_food.html', context)

    def post(self, request):
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.vendor = get_vendor(self.request)
            food_item.slug = slugify(food_item.food_title)
            form.save()
            messages.success(request, 'Food item created successfully!')
            return redirect('fooditems_by_category', food_item.category.id)


class EditFoodItemView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin, UpdateView):

    def test_func(self):
        return check_role_vendor(self.request.user)

    model = FoodItem
    template_name = 'vendor/edit_food.html'
    form_class = FoodItemForm
    success_message = 'Food item updated successfully!'
    context_object_name = 'food_item'

    def form_valid(self, form):
        food_item = form.save(commit=False)
        self.kwargs['category_id'] = food_item.category.id
        return super().form_valid(form)

    def get_success_url(self):
        category_id = self.kwargs['category_id']
        return reverse_lazy('fooditems_by_category', kwargs={'pk': category_id})


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food_item(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    category_id = food_item.category.id
    food_item.delete()
    messages.success(request, 'Food item has been deleted successfully!')
    return redirect('fooditems_by_category', category_id)
