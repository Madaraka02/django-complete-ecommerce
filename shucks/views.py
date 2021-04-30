from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic import View, DetailView, ListView
from .forms import AddressForm
from .models import  *

# Create your views here.
class catlistView(ListView):
    template_name = "category-products.html"
    context_object_name = 'catlist'
    # paginate_by = 24

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'items': Item.objects.filter(category__title=self.kwargs['category'])
        }
        return content


def home(request):
    items = Item.objects.filter(featured=True).order_by('-id')[:12]
    brand = Brand.objects.filter(best_seller=True)
    bests = Item.objects.filter(brand=True).order_by('-id')[:12]
    context = {
        'items': items,
        'bests': bests
    }
    return render(request, 'home.html', context)

def products(request):
    items = Item.objects.all().order_by('-id')
    paginator = Paginator(items, 18)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
    }
    return render(request, 'product.html', context)

def featured(request):
    items = Item.objects.filter(featured=True).order_by('-id')
    paginator = Paginator(items, 18)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'featured.html', context)
def best_seller(request):
    brand = Brand.objects.filter(best_seller=True)
    bests = Item.objects.filter(brand=True).order_by('-id')
    paginator = Paginator(bests, 18)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'best_seller.html', context)    


def details(request, id):
    item = Item.objects.get(id=id)
    related = Item.objects.filter(category=item.category).exclude(id=id)[:4]
    context = {
        'item': item,
        'related': related
    }
    return render(request, 'product-details.html', context)


def search(request):
    q = request.GET['q']
    context = {
        'data' : Item.objects.filter(title__icontains=q).order_by('-id'),
        'brand' : Brand.objects.filter(title__icontains=q).order_by('-id'),
        'category' : Category.objects.filter(title__icontains=q).order_by('-id')
    }

    return render(request, 'search.html', context)   

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.success(request, f"{item.title}'s was updated")
            return redirect('cart')
        else:
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item.title} was added to your cart")
            return redirect('cart')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, ordered_date=ordered_date)
        order.items.add(order_item)
        order.save()
        messages.success(request, f"{item.title} was added to your cart")
        return redirect('cart')    

def remove_from_cart(request, slug):  
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(order_item)
            order.save()
            messages.success(request, f"{item.title} was removed from your cart")
            return redirect('cart')
        else:
            messages.info(request, f"{item.title} was not in your cart")
            return redirect('cart') 
    else:
        messages.info(request, "You dont have any items in your cart")
        return redirect('products')                        
def remove_single_item_from_cart(request, slug):  
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.save()   
            return redirect('cart')
        else:
            messages.info(request, f"{item.title} was not in your cart")
            return redirect('cart') 
    else:
        messages.info(request, "You dont have any items in your cart")
        return redirect('products')    
class cartView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'cart.html', context)  

class checkoutView(View):
    def get(self, *args, **kwargs):
        # address = Address.objects.get(user=self.request.user, default=True)
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = AddressForm()
        context = {
            'form': form,
            'order': order
            # 'address':address
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = AddressForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                county = form.cleaned_data.get('county')
                location = form.cleaned_data.get('location')
                phone_number = form.cleaned_data.get('phone_number')
                save_info = form.cleaned_data.get('save_info')
                use_default = form.cleaned_data.get('use_default')

                address = Address(
                    user = self.request.user,
                    county = county,
                    location = location,
                    phone_number = phone_number
                )
                address.save()
                order.address = address
                order.save()
                
                if save_info:
                    address.default = True
                    address.save()
                
                order.address = address
                order.save()

                if use_default:
                    # address = Address.objects.get(user=self.request.user, default=True)
                    order.address = address
                    order.save()

                print(form.cleaned_data)
                messages.success(self.request, "Your order has been received we will respond within 24 hours")
                return redirect('cart')
            else:
                print(f'form_invalid') 
                return redirect('checkout')  
        except ObjectDoesNotExist:
            message.error(self.request, "you dont have an active order")         

