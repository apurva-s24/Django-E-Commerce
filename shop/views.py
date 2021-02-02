from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import PaytmChecksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'


# Create your views here.


def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nslides = n // 4 + ceil((n / 4) - (n // 4))

    all_products = []
    product_category = Product.objects.values('category', 'id')
    categories = {item['category'] for item in product_category}
    for cat in categories:
        products = Product.objects.filter(category=cat)
        n = len(products)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        all_products.append([products, range(1, nslides), nslides])

    # params = {'no_of_slides': nslides, 'range': range(1, nslides), 'product': products}
    # all_products = [[products, range(1, nslides), nslides], [products, range(1, nslides), nslides]]
    params = {'all_products': all_products}
    return render(request, 'shop/index.html', params)


def searchMatch(query, item):
    """ return True only if query matches the item """
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    all_products = []
    product_category = Product.objects.values('category', 'id')
    categories = {item['category'] for item in product_category}
    for cat in categories:
        producttemp = Product.objects.filter(category=cat)
        products = [item for item in producttemp if searchMatch(query, item)]
        n = len(products)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(products) != 0:
            all_products.append([products, range(1, nslides), nslides])
    params = {'all_products': all_products, 'msg': ''}
    if len(all_products) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contacts = Contact(name=name, email=email, phone=phone, desc=desc)
        contacts.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_description, 'time': item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "itemJson": order[0].items_json},
                                          default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "noitem"}')
        except Exception as e:
            return HttpResponse('{{"status": "error"}')

    return render(request, 'shop/tracker.html')


def productview(request, myid):
    # Fetch the product using the Id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/productview.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                      zip_code=zip_code, phone=phone, amount=amount)
        order.save()

        update = OrderUpdate(order_id=order.order_id, update_description="Your order has been placed")
        update.save()
        thank = True
        id1 = order.order_id
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id1': id1})
        # Request paytm to transfer the amount to your account after payment by user
        params = {
            'MID': 'YOUR-MERCHANT-KEY',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'worldpressplg',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        params['CHECKSUMHASH'] = PaytmChecksum.generateSignature(params, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'params': params})
    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = PaytmChecksum.verifySignature(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Order Successful')
        else:
            print('Order was not successful because ' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
    pass
