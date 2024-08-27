"""
URL configuration for muji project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('signup/',signup, name="signup"),
    path('product_class/<int:pk>/', product_class_detail, name='product_class_detail'),
    path('search/', search_items, name='search_items'),
    path('search-results/<str:query>/', search_results, name='search_results'), 
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('update_cart_quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('remove_from_cart/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('login/',login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path('profile/', profile_view, name='profile'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('success/', checkout_success, name='checkout_success'),
    path('cancel/', checkout_cancel, name='checkout_cancel'),
    path('item/<int:item_id>/add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('item/<int:item_id>/remove-from-wishlist/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', wishlist_view, name='wishlist_view'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

