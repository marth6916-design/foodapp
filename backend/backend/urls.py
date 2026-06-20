"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from foodapp.views import home,login_view,register_view,logout_view,menu,add_to_cart,cart,remove_from_cart,checkout,order_history,increase_qty,decrease_qty,tracking,manage_orders,dashboard,restaurants,restaurant_menu,food_detail
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('login/',login_view,name='login'),
    path('register',register_view,name='register'),
    path('logout/',logout_view,name='logout'),
    path('menu/', menu,name='menu'),
    path('cart/',cart,name='cart'),
    path('add-to-cart/<int:food_id>/',add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/',remove_from_cart,name='remove_from_cart'),
    path('checkout/',checkout,name='checkout'),
    path('order-history/',order_history,name='order_history'),
    path('increase-qty/<int:item_id>',increase_qty,name='increase_qty'),
    path('decrease-qty/<int:item_id>',decrease_qty,name='decrease_qty'),
    path('tracking/<int:order_id>',tracking,name='tracking'),
    path('manage-orders/',manage_orders,name='manage_orders'),
    path('dashboard/',dashboard,name='dashboard'),
    path('restaurants/', restaurants, name='restaurants'),
    path('food/<int:food_id>/', food_detail, name='food_detail'),
    path('restaurants/<int:restaurant_id>/', restaurant_menu, name='restaurant_menu'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
