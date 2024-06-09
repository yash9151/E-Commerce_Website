from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from django.views.decorators.csrf import csrf_exempt
from math import ceil
import json
from django.http import HttpResponse
from PayTm import Checksum

# MERCHANT_KEY = 'kbzk1DSbJiV_03p5';
MERCHANT_KEY = 'yWtPp&P4Gqh!lPTr';

# Create your views here.
def index(request):
    # fetches products from database
    products = Product.objects.all()
    print(products)
    n=len(products)
    nSlides = n//4 + ceil((n/4) - (n//4))
    # params = {'product' : products, 'no_of_slides':nSlides, 'range' : range(1, nSlides)}
    #
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]

    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds' : allProds}
    return render(request, "shop/index.html", params)

def about(request):
    return render(request, "shop/about.html")

def contact(request):
    thank = False
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request, "shop/contact.html", {'thank': thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, "shop/search.html")

def prodView(request, myid):
    # fetch the product using id
    product = Product.objects.filter(id=myid)
    print(product)

    return render(request, "shop/prodView.html", {'product': product[0]})

def checkout(request):
    if request.method == 'POST':
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, items_json=items_json,
                       amount=amount)
        order.save()
        update = OrderUpdate(order_id = order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, "shop/checkout.html", {'thank':thank, 'id':id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

            # 'MID': 'WorldP64425807474247',
            'MID': 'ffyvpw67039918604874',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, "shop/checkout.html")

#
@csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]
#
#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     # return HttpResponse("Done")
#     # pass
#     return render(request, 'shop/paymentstatus.html', {'response': response_dict})

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            form = request.POST
            response_dict = {}
            checksum = None  # Initialize checksum variable
            for key in form.keys():
                response_dict[key] = form[key]
                if key == 'CHECKSUMHASH':
                    checksum = form[key]  # Assign value to checksum

            if checksum is not None:  # Check if checksum is assigned a value
                verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
                if verify:
                    if response_dict['RESPCODE'] == '01':
                        print('Order successful')
                    else:
                        print('Order was not successful because: ' + response_dict['RESPMSG'])
                else:
                    print('Checksum verification failed')
            else:
                print('Checksum not found in the response')

            return render(request, 'shop/paymentstatus.html', {'response': response_dict})

        except Exception as e:
            return HttpResponse("Error in payment processing: " + str(e))

    return HttpResponse("Invalid request method")
