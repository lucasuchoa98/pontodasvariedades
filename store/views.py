from django.http import JsonResponse
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.views.generic import DetailView, ListView, TemplateView
import json
import datetime
from django.db.models import Q
from allauth.account.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages


"""
class StoreView(ListView):
    model = Product
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        cartItems = data['cartItems']
        context['cartItems'] = cartItems

        return context
"""

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query))
    category_query = request.GET.get('category')
    if category_query:
        products = products.filter(Q(category__icontains=category_query))
    context = {'products':products,'cartItems':cartItems}
    return render(request, 'store/store.html', context)

class SearchResultsView(ListView):
    model = Product
    template_name = 'search_results.html'

    def get_queryset(self,**kwargs):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(name__icontains=query)
        )
        return object_list 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        cartItems = data['cartItems']
        context['cartItems'] = cartItems

        return context


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

@login_required
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

class ItemDetailView(DetailView):
    model = Product
    template_name = "store/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        
        cartItems = data['cartItems']
        context['cartItems'] = cartItems

        return context

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)
    customer, created = Customer.objects.get_or_create(name = request.user.username, email = request.user.email
        )
    customer.save()

    product = Product.objects.get(id= productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order = order, product= product)

    if action=='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action=='remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('O Item foi adicionado', safe=False)

#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        email = request.user.email
        customer, created = Customer.objects.get_or_create(
            email=email,
        )
        customer.name = request.user.username
        customer.save()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    return JsonResponse('Pagamento completo', safe=False)

from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template

def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems':cartItems}


    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            content = request.POST.get('content', '')
            assunto = request.POST.get('subject', '')

            contato = Contato(contact_name=contact_name, contact_email=contact_email, content=content, subject= assunto)
            contato.save(0)
            messages.info(request, 'Sua mensagem foi enviada com sucesso!')
            return redirect('store:contato')
    else:
        form = ContactForm()

        return render(request, 'store/contato.html', {
        'form': form,
        })
