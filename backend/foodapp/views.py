from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Food,Cart,Order,OrderItem,Restaurant,Review
from django.contrib.auth.decorators import login_required

def home(request):
    total_restaurants = Restaurant.objects.count()
    total_foods = Food.objects.count()
    total_users = User.objects.count()
    popular_foods = Food.objects.all()[:4]
    return render(request, 'home.html', {
        'total_restaurants': total_restaurants,
        'total_foods': total_foods,
        'total_users': total_users,
        'popular_foods': popular_foods
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()
        messages.success(request, 'Account created! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def menu(request):
    category = request.GET.get('category', 'All')
    search = request.GET.get('search', '')
    
    foods = Food.objects.all()
    
    if category != 'All':
        foods = foods.filter(category=category)
    
    if search:
        foods = foods.filter(name__icontains=search)
    
    categories = ['All', 'Burgers', 'Pizza', 'Drinks', 'Sides', 'Desserts']
    return render(request, 'menu.html', {
        'foods': foods,
        'categories': categories,
        'selected': category,
        'search': search
    })

@login_required(login_url='login')
def add_to_cart(request, food_id):
    food = Food.objects.get(id=food_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, food=food
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('menu')

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    
    if request.method == 'POST':
        address = request.POST['address']
        payment_method = request.POST['payment_method']
        
        order = Order.objects.create(
            user=request.user,
            total=total,
            address=address,
            payment_method=payment_method
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food=item.food,
                quantity=item.quantity,
                price=item.food.price
            )
        cart_items.delete()
        return redirect('order_history')
    
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required(login_url='login')
def increase_qty(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def decrease_qty(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def tracking(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'tracking.html', {'order': order})

def manage_orders(request):
    if not request.user.is_staff:
         return redirect('home')
    orders = Order.objects.all().order_by('-created_at')
    if request.method == 'POST':
         order_id = request.POST['order_id']
         status = request.POST['status']
         order = Order.objects.get(id=order_id)
         order.status = status
         order.save()
         return redirect('manage_orders')
    return render(request, 'manage_orders.html', {'orders': orders})


def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    
    total_orders = Order.objects.count()
    total_revenue = sum(o.total for o in Order.objects.all())
    total_users = User.objects.count()
    total_foods = Food.objects.count()
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    return render(request, 'dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_foods': total_foods,
        'recent_orders': recent_orders
    })

def restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants.html', {'restaurants': restaurants})

def restaurant_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    foods = Food.objects.filter(restaurant=restaurant)
    category = request.GET.get('category', 'All')
    if category != 'All':
        foods = foods.filter(category=category)
    categories = ['All', 'Burgers', 'Pizza', 'Drinks', 'Sides', 'Desserts']
    return render(request, 'restaurant_menu.html', {
        'restaurant': restaurant,
        'foods': foods,
        'categories': categories,
        'selected': category
    })

def food_detail(request, food_id):
    food = Food.objects.get(id=food_id)
    reviews = Review.objects.filter(food=food).order_by('-created_at')
    
    # Calculate average rating
    if reviews.exists():
        avg_rating = round(sum(r.rating for r in reviews) / reviews.count())
    else:
        avg_rating = 0
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST['rating']
        comment = request.POST['comment']
        Review.objects.create(
            user=request.user,
            food=food,
            rating=rating,
            comment=comment
        )
        messages.success(request, 'Review submitted!')
        return redirect('food_detail', food_id=food_id)
    
    return render(request, 'food_detail.html', {
        'food': food,
        'reviews': reviews,
        'avg_rating': avg_rating
    })