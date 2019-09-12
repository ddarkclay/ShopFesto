from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
import json
import requests

# Create your views here.

def register(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username= request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		user = User.objects.all()

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
			if password1 == password2:
				if User.objects.filter(username=username).exists():
					params = {'first_name':first_name, 'last_name':last_name, 'email':email, 'error':"username",'msg':"Username already Taken"}
					return render(request, 'account/register.html', params)
				elif User.objects.filter(email=email).exists():
					params = {'first_name':first_name, 'last_name':last_name, 'username':username,'error':"email", 'msg':"Email already Taken"}
					return render(request, 'account/register.html', params)
				else:
					user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name,last_name=last_name)
					user.save()
					print('User Created')
					return redirect('/account/login')
			else:
				params = {'first_name':first_name, 'last_name':last_name, 'username':username ,'email':email, 'error':"password", 'msg':"Password Not Matching"}
				return render(request, 'account/register.html', params)
			return redirect('/account/login')
		else:
			return HttpResponse('<script>alert("Please Fill Recaptcha");document.location = "/register";</script>')	
	
	else:
		return render(request, 'account/register.html')

def login(request):
	user = auth.authenticate()
	if user is not None:
		if request.method == 'POST':
			username= request.POST['username']
			password = request.POST['password']
			user = auth.authenticate(username=username, password=password)
			if user is not None:
				auth.login(request, user)
				valid = True
				print(f"User Login : {valid}")
			else:
				params = {'username':username, 'error':"userpass", 'msg':"Invalid Username and Password"}
				print(f"User Login : {valid}")
				return render(request, 'account/login.html', params)
			return redirect('/shop')
		else:
			return render(request, 'account/login.html')
	else:
		return redirect('/shop')

# def logout(request):
# 	auth.logout(request)
# 	return redirect('/')
