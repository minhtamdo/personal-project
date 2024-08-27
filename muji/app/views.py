from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from decouple import config

stripe.api_key = config('STRIPE_SECRET_KEY')

# Create your views here.
def index(request):
    return render(request,"index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or reverse("view_cart")
            return redirect(next_url)
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password.",
                "next": request.POST.get('next') or request.GET.get('next') or reverse("view_cart")
            })
    else:
        next_url = request.GET.get('next') or reverse("view_cart")
        return render(request, "login.html", {"next": next_url})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.email = form.cleaned_data.get('email')
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.address = form.cleaned_data.get('address')
        user.profile.phone_number = form.cleaned_data.get('phone_number')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'signup.html', {'form': form})

def product_class_detail(request, pk):
    
    product_class = get_object_or_404(ProductClass, pk=pk)
    items = Item.objects.filter(product_class=product_class)

    items_with_prices = []
    for item in items:
        first_product = item.general_name.first()  # Fetch the first associated product
        if first_product:
            items_with_prices.append({
                'item': item,
                'price': first_product.price,
            })

    context = {
        'product_class': product_class,
        'items_with_prices': items_with_prices,
    }
    return render(request, 'product_class_detail.html', context)

def search_items(request):
    query = request.GET.get('q')
    if query:
        return redirect('search_results', query=query)
    else:
        return redirect('index')  # Redirect back to index if no query provided

def search_results(request, query):
    items = Item.objects.filter(name__icontains=query)
    items_with_prices = []
    for item in items:
        first_product = item.general_name.first()  # Fetch the first associated product
        if first_product:
            items_with_prices.append({
                'item': item,
                'price': first_product.price,
            })
    context = {
        'items_with_prices': items_with_prices,
        'query': query
    }
    return render(request, 'search_results.html', context)

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    products = Product.objects.filter(name=item)
    
    unique_colors = Color.objects.filter(product_color__in=products).distinct()
    unique_sizes = Size.objects.filter(product_size__in=products).distinct().order_by('id')

    default_image_url = item.image.url if item.image else (products.first().image.url if products.first().image else None)

    added_to_cart = request.GET.get('added_to_cart')

    # Collect all images for the gallery
    product_images = [product.image.url for product in products if product.image]

    # Handle comment form submission
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.item = item
                comment.user = request.user
                comment.save()
                return redirect('item_detail', item_id=item.id)  # Redirect to avoid form resubmission
        else:
            # Redirect to login page if user is not authenticated
            return redirect(f'{reverse("login")}?next={request.path}')
    else:
        form = CommentForm()

    # Retrieve existing comments
    comments = item.comments.all()

    return render(request, 'item_detail.html', {
        'item': item,
        'products': products,
        'unique_colors': unique_colors,
        'unique_sizes': unique_sizes,
        'added_to_cart': added_to_cart,
        'default_image_url': default_image_url,
        'product_images': product_images,
        'form': form,
        'comments': comments,  # Pass comments to the template
    })



@login_required(login_url='/login/')
def add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        color_id = request.POST.get('color_id')
        size_id = request.POST.get('size_id')
        quantity = int(request.POST.get('quantity', 1))

        if not item_id:
            messages.error(request, "Item ID is missing.")
            return redirect('index')

        item = get_object_or_404(Item, id=item_id)
        color = get_object_or_404(Color, id=color_id)
        size = get_object_or_404(Size, id=size_id)
        product = get_object_or_404(Product, name=item, color=color, size=size)

        # Check if there's enough stock available
        if product.stock < quantity:
            messages.error(request, f'Not enough stock for {item.name}. Only {product.stock} left.')

        profile = request.user.profile

        # Check if the item is already in the cart
        cart_item, created = Cart.objects.get_or_create(
            owner=profile,
            name=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # Update the quantity if the item is already in the cart
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, f'Added {item.name} to the cart!')

        # Redirect to view_cart after adding item
        return redirect('view_cart')

    # If not POST request, redirect to index
    return redirect('index')

@login_required(login_url='/login/')
def view_cart(request):
    profile = request.user.profile
    cart_items = Cart.objects.filter(owner=profile)
    
    total_price = 0
    for item in cart_items:
        # Use the property method to get the total price
        total_price += item.total_price

    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'stripe_publishable_key': settings.STRIPE_PUBLIC_KEY
    })

@login_required(login_url='/login/')
def update_cart_quantity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_id = data.get('cart_id')
            quantity = int(data.get('quantity'))
            
            # Ensure cart_id and quantity are valid
            if cart_id is None or quantity is None:
                return JsonResponse({'error': 'Invalid data'}, status=400)
            
            # Retrieve cart item
            cart_item = get_object_or_404(Cart, id=cart_id, owner=request.user.profile)
            
            if quantity <= 0:
                cart_item.delete()
                response_data = {
                    'status': 'removed',
                    'total_price': float(get_cart_total_price(request.user.profile))
                }
            else:
                cart_item.quantity = quantity
                cart_item.save()
                response_data = {
                    'status': 'updated',
                    'total_price': float(get_cart_total_price(request.user.profile)),
                    'item_total_price': float(quantity * cart_item.name.price)
                }
            
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def get_cart_total_price(profile):
    cart_items = Cart.objects.filter(owner=profile)
    return sum(item.quantity * item.name.price for item in cart_items)

@login_required(login_url='/login/')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, owner=request.user.profile)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

@login_required(login_url='/login/')
def checkout(request):
    if request.method == 'POST':
        try:
            cart_items = Cart.objects.filter(owner=request.user.profile)
            for item in cart_items:
                product = item.name
                if product.stock < item.quantity:
                    return JsonResponse({'error': f'Not enough stock for {product.name.name}'}, status=400)
                product.stock -= item.quantity
                product.save()
            
            # Clear the cart after successful checkout
            cart_items.delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@login_required(login_url='/login/')        
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            # Get the user's profile and cart items
            profile = request.user.profile
            cart_items = Cart.objects.filter(owner=profile)

            # Create Stripe checkout session line items
            line_items = []
            for item in cart_items:
                product = item.name
                if product.stock < item.quantity:
                    return JsonResponse({'error': f'Not enough stock for {product.name.name}'}, status=400)
                product.stock -= item.quantity
                product.save()
                line_items.append({
                    'price_data': {
                        'currency': 'jpy',  # Currency
                        'product_data': {
                            'name': product.name,
                        },
                        'unit_amount': int(product.price),  # Price in cents
                    },
                    'quantity': item.quantity,
                })

            # Create the Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )

            # Return the session ID as a JSON response
            return JsonResponse({'id': checkout_session.id})

        except Exception as e:
            # Log error and return error response
            print(f"Error creating checkout session: {e}")  # Logging the error
            return JsonResponse({'error': str(e)}, status=500)
    
    # Return error response if request method is not POST
    return JsonResponse({'Processing': 'Click return to continue'}, status=405)

@login_required(login_url='/login/')
def checkout_success(request):
    # Process the successful payment here, e.g., clearing the cart
    profile = request.user.profile
    Cart.objects.filter(owner=profile).delete()
    return render(request, 'checkout_success.html')

@login_required(login_url='/login/')
def checkout_cancel(request):
    return render(request, 'checkout_cancel.html')


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form
    }

    return render(request, 'profile.html', context)

@login_required
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check if the item is already in the wishlist
    if not Wishlist.objects.filter(owner=profile, item=item).exists():
        Wishlist.objects.create(owner=profile, item=item)
    
    return redirect('item_detail', item_id=item.id)

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Remove the item from the wishlist if it exists
    wishlist_item = Wishlist.objects.filter(owner=profile, item=item).first()
    if wishlist_item:
        wishlist_item.delete()
    
    return redirect('item_detail', item_id=item.id)


@login_required
def wishlist_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    items = Wishlist.objects.filter(owner=profile).values_list('item', flat=True)
    items = Item.objects.filter(id__in=items)
    return render(request, 'wishlist.html', {'items': items})