from django.shortcuts import render
from .models import Contact,User
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
				name=request.POST['name'],
				email=request.POST['email'],
				mobile=request.POST['mobile'],
				remarks=request.POST['remarks']
			)
		msg="Contact saved successfully"
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'msg':msg,'contacts':contacts})
	else:
		contacts=Contact.objects.all().order_by("-id")[:3]	
		return render(request,'contact.html',{'contacts':contacts})	

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:	
				User.objects.create(
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=request.POST['password']
					)
				msg="User Sign Up Successfully"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg="password & Confirm password does not matched"	
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'index.html')
			else:
				msg="incorrect password"
				return render(request,'login.html',{'msg':msg})	
		except:
			msg="Email NOt Registered"
			return render(request,'login.html',{'msg':msg})		
	else:	
		return render(request,'login.html')	

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		msg="User logged Out Successfully"
		return render(request,'login.html',{'msg':msg})	
	except:
		msg="User logged Out Successfully"
		return render(request,'login.html',{'msg':msg})	

def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				if user.password!=request.POST['new_password']:
					user.password=request.POST['new_password']
					user.save()
					del request.session['email']
					del request.session['fname']
					msg="password changed Successfully"
					return render(request,'login.html',{'msg':msg})
				else:
					msg="your new password can't be from your old password"
					return render(request,'change-password.html',{'msg':msg})
			else:
				msg="new password & old password does not matched"
				return render(request,'change-password.html',{'msg':msg})
		else:
			msg="old password does not matched"
			return render(request,'change-password.html',{'msg':msg})					
	else:
		return render(request,'change-password.html')	

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject="OTP For forgot password"
			message="Hello "+user.fname+", Your OTP For forgot password Is "+str(otp)
			to=[user.email,]
			send_mail(subject, message, settings.EMAIL_HOST_USER, to)
			request.session['email']=user.email
			request.session['otp']=otp
			msg="OTP Sent Successfully"
			return render(request,'otp.html',{'msg':msg})
		except:
			msg="Email Not Registered"
			return render(request,'forgot-password.html',{'msg':msg})	
	else:	
		return render(request,'forgot-password.html')

def verify_otp(request):
	otp1=int(request.POST['otp'])
	otp2=int(request.session['otp'])	

	if otp1==otp2:
		del request.session['otp']
		return render(request,'new-password.html')	
	else:
		msg="Invalid OTP"	
		return render(request,'otp.html',{'msg':msg})

def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		user=User.objects.get(email=request.session['email'])
		user.password=request.POST['new_password']
		user.save()
		msg="Password Updated Successfully"
		del request.session['email']
		return render(request,'login.html',{'msg':msg})
	else:
		msg="New Password & Confirm New Password Does Not Matched"	
		return render(request,'new-password.html',{'msg':msg})