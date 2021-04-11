from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact , Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def index(request):
    # prod = Product.objects.all()
    # n = len(prod)
    # nslides = n//4 + ceil((n/4 - n//4))
    # params = {"No.of slides": nslides, 'range': range(1,nslides), "products": prod }
    # allprods = [[prod, range(1,nslides), nslides],
    #             [prod, range(1,nslides), nslides],]
    allprods = []
    catprods = Product.objects.values('category')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4 - n // 4))
        allprods.append([prod, range(1, nslides), nslides])
    params = {"allprod": allprods}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name= name, email= email, phone= phone, desc= desc)
        contact.save()
        thanks = True
        return render(request, 'shop/contact.html', {'thanks': thanks})
    return render(request, 'shop/contact.html')

@cache_page(60 * 15)
@csrf_protect
def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('OrderId')
        email = request.POST.get('email')
        print(orderId, email)
        try:
            orderRequest = Order.objects.filter(order_id= orderId, email= email)
            print(orderRequest)
            if len(orderRequest)>0:
                update = OrderUpdate.objects.filter(order_id= orderId)
                updates = []
                print(update)
                for item in update:
                    # updates.append({'text': item.desc, 'date': item.timestamp})
                    # response = json.dumps(updates, default=str)
                    # print(response["text"])
                    params = {"desc": item.desc, "date": item.timestamp}
                    print(params)
                    return render(request, 'shop/tracker.html', params)
            else:
                # pass
                return HttpResponse("error")
        except Exception as e:
            return HttpResponse("error")

    return render(request, 'shop/tracker.html')


def search(request):
    return HttpResponse("We are at search..!!")


def productView(request, id):
    # fetch the product using product id
    product = Product.objects.filter(id=id)
    params = {"prod": product[0]}
    return render(request, 'shop/products.html', params)


def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        order_json = request.POST.get('items_json', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        add1 = request.POST.get('add1', '')
        add2 = request.POST.get('add2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip', '')
        order = Order(name= name, order_json= order_json , email= email, phone= phone, add1= add1, add2= add2, city= city, state= state, zip_code= zip_code)
        order.save()
        thanks = True
        id = order.order_id
        update = OrderUpdate(order_id= order.order_id, desc="Your order has been placed.")
        update.save()
        print(order_json)
        # order_for_price = Product.Obects.filter(prod_name= )

        params = {'thanks': thanks, 'id': id}
        return render(request, 'shop/checkout.html', params)
    return render(request, 'shop/checkout.html')
