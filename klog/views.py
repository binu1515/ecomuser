from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from klog.models import Categrory, Order, product, user, Cart, Cartitems, OrderItem
from .forms import CartAddProductForm, OrderCreateForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
#from .cart import Cart
# Create your views here.

#def index(request) :
    #return render(request, 'index.html')

def signup(request):
    user=request.session.get('username')
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if (password1 == password2):
            if User.objects.filter(username=username):
                messages.info(request, "username already in use")
                return redirect('/')
            elif User.objects.filter(email=email):
                messages.info(request, "Email already in use")
                return redirect('/')
            else:
                users = User.objects.create_user(
                    first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
                users.save()
                return redirect('/')
        else:
            messages.info(request, "Password not matching")
        return redirect('/') 
    elif(user):
        return redirect('/')
    else:
        return render(request, "signup.html",{'user':user})

def login(request):
    cart = Cart(request) 
    user=request.session.get('username')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            request.session['id'] = user.id
            request.session['username']=user.username
        
            return JsonResponse({'success': True},safe=False)
        else:
            
            return JsonResponse({'success': False},safe=False)
    elif(user):
        if'next'in request.POST:
            return redirect(request.POST.get('next'))
        else:
          return redirect('/create')
    elif(user):
        return redirect('/signup')
    else:
        return render(request, "login.html",{'user':user ,'cart':cart})


def index(request):
    user=request.session.get('username')
    products = product.objects.all()
    categories = Categrory.objects.all()
    return render(request, "index.html", {'products': products, 'user': user, 'cart': cart, 'categories':categories})

def detail(request, category_id, product_id):
    cart = Cart(request) 
    produc = get_object_or_404(product, pk=product_id)
    
    categories = Categrory.objects.all()
    return render(request, 'detail.html', {'category_id': category_id, 'produc': produc,
                                           'product_id': product_id, 'categories': categories, 'cart':cart})


def cart(request):
    cart = Cart(request) 
    product_ids = request.session.get('cart', [])
    categories = Categrory.objects.all()
    
    products = product.objects.filter(id__in=product_ids)
    cartvalue=products.count()
    total2 = (product.objects.filter(id__in=product_ids).values_list('quantity', flat=True))
    total = sum(product.objects.filter(id__in=product_ids).values_list('price', flat=True))
    quantity = request.POST.get('quantity')
   
    print(quantity)
    
    
    #total = total1*cartvalue
    form = CartAddProductForm 

    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
         quantity = form.data['quantity']
         order = Order.objects.create(quantity=quantity, total=float(total))

         order.products.set(products)

         #request.session['cart'].clear()

        return redirect('/')
    return render(request, 'cart.html', {'products': products,'form':form, 'total': total, 'total2':total2,'categories': categories})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)  # create a new cart object passing it the request object 
    produc = get_object_or_404(product, id=product_id) 
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(produc=produc, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('klog:cart')


def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id not in cart:
        cart.append(product_id)
        request.session['cart'] = cart
        produc = get_object_or_404(product, pk=product_id)
    else:
        produc = None

    return render(request, 'item-added.html', {'cart': cart, 'produc': produc})


def cartdelete(request, product_id):
    cart = request.session['cart']
    cart.remove(product_id)
    request.session['cart'] = cart
    produc = get_object_or_404(product, pk=product_id)
    return render(request, 'cartdelete.html', {'produc': produc})




def cartitems(request, product_id):
    products = get_object_or_404(product, id=product_id)
    return render(request, 'cartitems.html')


def checkout(request, id):
    order = get_object_or_404(Order, id=id)
    products = order.products.all()
    return render(request, 'checkout.html', {'products': products, 'id': id})


def Logout(request):
    try:
        request.session.flush()
    except:
        pass    
    return redirect("/")   




def cart_detail(request):
    cart = request.session['cart']
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart.html', {'cart': cart})

def payment(request):
    return render(request, 'payment.html')

@login_required(login_url='/login')
def order_create(request):
    cart = request.session['cart']
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price= ['price'],
                    quantity=item['quantity']
                )
            cart.clear()
        return render(request, 'checkout.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'create.html', {'form': form})


def addtocart(request):
    if request.method == 'POST':
        if request.customer.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.customer.id, product_id=prod_id)):
                    return JsonResponse({'status':"product already in cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status':"product added successfully"})
                    else:
                        return JsonResponse({'status':"only"+ str(product_check.quantity) +" quantity available"})
            else:
                return JsonResponse({'status':"login to continue"})

    return redirect('/')


#def detail(request, category_id, product_id):
    #if(Categrory.objects.filter(pk=category_id)):
        #if(product.objects.filter(pk=product_id)):
            #products = product.objects.filter(pk=product_id).first
            #context = {'products':products}
        #else:
            #messages.error(request, "no such category")
            #return redirect('index')
    #else:
        #messages.error(request, "No such category")
        #return redirect('index')
    #return render(request, "view.html", context)


    