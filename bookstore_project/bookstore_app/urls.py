from django.urls import path
from django.contrib.auth import views as auth_views # Use built-in auth views
from . import views # Import your app's views

urlpatterns = [
    # Book Views
    path('', views.book_list, name='book_list'), # Homepage shows books

    # Cart Views
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'), # Optional: Add remove functionality
    path('cart/checkout/', views.checkout, name='checkout'),

    # Authentication Views (using Django's built-in views)
    path('login/', auth_views.LoginView.as_view(template_name='bookstore_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # No template needed for default logout view

    # Add other views like book detail if needed
]