from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.FoodItemsByCategoryListView.as_view(), name='fooditems_by_category'),

    # Category CRUD
    path('menu-builder/category/add/', views.AddCategoryFormView.as_view(), name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.EditCategoryView.as_view(), name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # Food item CRUD
    path('menu-builder/food/add/', views.AddFoodView.as_view(), name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.EditFoodItemView.as_view(), name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food_item, name='delete_food'),



]