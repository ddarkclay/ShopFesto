from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Productheader, Product, Contact, Order, OrderUpdate, Category, Coupon
import json
import requests
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
# from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

MERCHANT_KEY = 'rKx0db2cc71VonCf'

def index(request):
	prodheaders = Productheader.objects.all()
	category = Category.objects.all()
	allProds = []
	catprods = Product.objects.values('category')
	# print(catprods)
	cats = {item['category'] for item in catprods}
	# print(cats)
	for cat in cats:
		prod = Product.objects.filter(category=cat)
		print(prod)
		n = len(prod)
		nSlides = n // 4 + ceil((n / 4) - (n // 4))
		allProds.append([prod, range(1, nSlides), nSlides])
		params = {'allProds':allProds, 'prodheaders':prodheaders, 'category':category}
	return render(request, 'shop/index.html', params)

def searchMatch(query, item):
	'''return true only if query matches the item'''
	if query.lower() in item.desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower() \
			and query.lower() in item.desc or query.lower() in item.product_name or query.lower() in item.category:
		return True
	else:
		return False


def search(request):
	query = request.GET.get('search')
	allProds = []
	catprods = Product.objects.values('category')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prodtemp = Product.objects.filter(category=cat)
		prod = [item for item in prodtemp if searchMatch(query, item)]
		n = len(prod)
		nSlides = n // 4 + ceil((n / 4) - (n // 4))
		if len(prod) != 0:
			allProds.append([prod, range(1, nSlides), nSlides])
	params = {'allProds': allProds}
	if len(allProds) == 0 or len(query)<2:
		params = {'msg': "Please make sure to enter relevant search query"}
	return render(request, 'shop/search.html', params)

def sale(request):
	products = Product.objects.all()
	# cat = Product.objects.filter(category=products.category[0])
	# category = Product.objects.filter(category=cat)
	return render(request, 'shop/sale.html', {'products':products})

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
	thanks = False
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		message = request.POST.get('message')
		# Recaptcha Stuff
		clientkey = request.POST['g-recaptcha-response']
		secretkey = '6Lc6WK0UAAAAAJgkZzc5mQIJ26vllxIZ2pxUde2K'
		captchData = {
			'secret': secretkey,
			'response':clientkey
		}
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchData)
		response = json.loads(r.text)
		verify = response['success']
		# print('Your success is : ', verify)
		if verify:
			contact = Contact(name=name, email=email, phone=phone, message=message)
			contact.save()
			thanks = True
		else:
			return HttpResponse('<script>alert("Please Fill Recaptcha");document.location = "/shop/contact";</script>')
	return render(request, 'shop/contact.html', {'thanks':thanks})

def tracker(request):
	if request.method == 'POST':
		orderId = request.POST.get('orderId', '');
		email = request.POST.get('email', '');
		print(f"{orderId} and {email}")
		try:
			order = Order.objects.filter(order_id=orderId, email=email)
			if len(order)>0:
				update = OrderUpdate.objects.filter(order_id=orderId)
				updates = []
				for item in update:
					updates.append({'text': item.update_desc, 'time': item.timestamp})
					response = json.dumps({"status":"success", "updates":updates, "itemJson":order[0].item_json}, default=str)
				return HttpResponse(response)
			else:
				return HttpResponse('{"status":"noitem"}')
		except Exception as e:
			return HttpResponse('{"status":"error"}')
	return render(request, 'shop/tracker.html')


def productview(request, myid):
	# Fetch the  product using Id
	product = Product.objects.filter(product_id=myid)
	products = Product.objects.filter(category=product[0].category)
	print(products)
	return render(request, 'shop/prodview.html', {'product':product[0], 'products':products})

@login_required
def checkout(request):
	param = {}
	if request.method == 'POST':
		coupon_code = request.POST['coupon-code'].upper()
		coupon = Coupon.objects.filter(coupon_txt=coupon_code)
		if coupon:
			# discount = Coupon.objects.values('discount')
			c = Coupon.objects.get(coupon_txt=coupon_code)
			discount = c.discount
			print(discount)
			param = {'msg':"Valid Coupon"}
		else:
			param = {'msg':"Invalid Coupon"}
	return render(request, 'shop/checkout.html', param)

def customer_details(request):
	if request.method == 'POST':
		item_json = request.POST.get('itemJson', '')
		name = request.POST.get('name', '')
		amount = request.POST.get('amount', '')
		print(amount)
		email = request.POST.get('email', '')
		address = request.POST.get('add_1', '') + " " + request.POST.get('add_2', '')
		city = request.POST.get('city', '')
		state = request.POST.get('state', '')
		zip_code = request.POST.get('zip_code', '')
		phone = request.POST.get('phone', '')
		order = Order(item_json=item_json, name=name, amount=amount, email=email, address=address, city=city,
			state=state, zip_code=zip_code, phone=phone)
		order.save()
		update = OrderUpdate(order_id=order.order_id, email=email, update_desc="The order has been placed")
		update.save()
		id = order.order_id
		thank = True
		# return render(request, 'shop/customer_details.html', {'thank':thank, 'id':id})
		# Request PayTm to transfer the amount to my account after payment by user
		param_dict = {
				'MID': 'QStzkN37825458068760',
				'ORDER_ID': str(order.order_id),
				'TXN_AMOUNT': str(amount),
				'CUST_ID': email,
				'INDUSTRY_TYPE_ID': 'Retail',
				'WEBSITE': 'WEBSTAGING',
				'CHANNEL_ID': 'WEB',
				'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
		}
		param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
		return render(request, 'shop/paytm.html', {'param_dict': param_dict})
	return render(request, 'shop/customer_details.html')

@login_required
def profile(request):
	return render(request, 'shop/profile.html')

@csrf_exempt
def handlerequest(request):
# paytm will send you post request here
	form = request.POST
	response_dict = {}
	for i in form.keys():
		response_dict[i] = form[i]
		if i == 'CHECKSUMHASH':
			checksum = form[i]

	verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
	if verify:
		if response_dict['RESPCODE'] == '01':
			# print(order)
			print('Order Successful')
		else:
			print('Order was not successful because' + response_dict['RESPMSG'])
	return render(request, 'shop/paymentstatus.html', {'response': response_dict})



