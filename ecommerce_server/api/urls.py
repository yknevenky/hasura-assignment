from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_cart_items_by_user_id),
    path('signup/', views.sign_up),
    path('signin/', views.sign_in),
    path('get-all-products/', views.get_all_products, name='get_all_products'),

    path('add-product/', views.add_product, name='add_product'),
    path('update-product/<str:product_id>/', views.update_product, name='update_product'),
    path('delete-product/<str:product_id>/', views.delete_product, name='delete_product'),
    path('get-all-categories/', views.get_all_categories, name='get_all_categories'),

    path('add-category/', views.add_category, name='add_category'),
    path('update-category/<str:category_id>/', views.update_category, name='update_category'),
    path('delete-category/<str:category_id>/', views.delete_category, name='delete_category'),
    path('create-cart/', views.create_cart, name='create_cart'),
    path('add-to-cart/', views.add_cart_item, name='add_to_cart'),
    path('remove-from-cart/', views.remove_cart_item, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('add-inventory/', views.add_inventory, name='add_inventory'),
    path('update-inventory/', views.update_inventory, name='update_inventory'),
    path('view-orders/<str:user_id>/', views.view_orders, name='view_orders'),
]