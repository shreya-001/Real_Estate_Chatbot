from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
#changes here down
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, get_token
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect, get_token,csrf_exempt
import sys
sys.path.append("..")
from Utils.response_main import predict


# import logging

# # Set up logging
# logger = logging.getLogger(__name__)



class IndexPageView(TemplateView):
    template_name = 'main/home1.html'

@csrf_protect
def page_view(request):
    return render(request, 'layouts/default/page.html')

class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
@login_required(login_url='login')
#signup
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST or None)
        if form.is_valid():

            #trail changes

            # form.first_name = fname
            # form.last_name = lname
            uname = request.POST.get('username')
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            form = User.objects.create_user('username', 'email', 'pass1')
            
            print(uname, email, pass1, pass2)
            #changes till here 
            user = form.save()
            auth_login(request, user)
            # HttpResponse(request, "Your account has been successfully created.")
            return redirect('login')
        else:
            form = SignupForm()
        return render(request, 'accounts/signup.html', {'form': form})

#login page
# def user_login(request):
#     #changes start 
#     def get(self, request):
#         return render(request, 'login.html')
    
#     def post(self, request):
#         csrf_token = get_token(request)
#         print("CSRF Token:", csrf_token)
#     #changes end 
    
#     # Check if 'user_type' is passed via GET or POST
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         #changes made from here
#         if form.is_valid():
#             email = request.POST.get('email')
#             # pass1 = form.cleaned_data['pass1']
#             pass1 = request.POST.get('pass1')
#             user = authenticate(request, email = email, pass1 = pass1)
#             #changes made here if user is now if user is not none
#             if user is not none:
#                 login(request, user)
#                 fname = user.first_name
#                 return redirect('home1')
#         else:
#             form = LoginForm()
#             HttpResponse("username or password incorrect.")
#             # \source\accounts\templates\accounts\log_in.html
#             # simple-django-login-and-register (1)\simple-django-login-and-register\source\accounts\templates\accounts\log_in.html
#             return render(request, 'accounts/log_in.html', {'fname': fname, 'user_type': user_type})
        #tohere       
# after login the user x


#changes made in this function


# def user_login(request):
#     # Check if 'user_type' is passed via GET or POST
#     # user_type = request.GET.get('user_type') or request.POST.get('user_type')

#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = request.POST.get('email')
#             pass1 = request.POST.get('pass1')
#             user = authenticate(request, email=email, password=pass1)  # correct field name to 'password'
#             if user is not None:
#                 login(request, user)
#                 fname = user.first_name
#                 return redirect('home1')
#             else:
#                 return HttpResponse("Username or password incorrect.")
#         else:
#             return render(request, 'accounts/log_in.html', {'form': form, 'user_type': user_type})

#     else:
#         form = LoginForm()
#         return render(request, 'accounts/log_in.html', {'fname': fname, 'user_type': user_type})

def user_login(request):
    print('Testttttt')
    # user_type = request.GET.get('user_type') or request.POST.get('user_type')
    # print(user_type)
    # if request.method == 'POST':
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         # user = authenticate(request, username=username, password=password)
    #         if (username is not None) and (password is not None):
                
    #             if username == 'customer':
    #                 return redirect('customer_login')
    #             elif username == 'realtor':
    #                 return redirect('realtor_login')
    #             else:
    #                 return HttpResponseBadRequest("Invalid user type")
    #         else:
    #             return HttpResponse("Username or password incorrect.")
    #     else:
    #         # Handle form errors if needed
    #         user_type = request.GET.get('user_type') or request.POST.get('user_type')
    #         print(user_type)
    #         return render(request, 'accounts/log_in.html', {'form': form, 'user_type': user_type})
            

    # else:  # GET request handling
    #     form = AuthenticationForm()
    #     user_type = request.GET.get('user_type') or request.POST.get('user_type')
    #     login_form = LoginForm()  # Your custom login form instance

    #     return render(request, 'accounts/log_in.html', {'form': login_form, 'user_type': user_type})





#@login_required(login_url='login/realtor/')
#changes begin 
def realtor(request):
    is_realtor = False
    if request.user.is_authenticated: 
        is_realtor = request.user.groups.filter(name = "Realtors").exists()
    return render(request, 'main/realtor.html', {'is_realtor' : is_realtor})
    # profile = UserProfile.objects.get(user=request.user)
    # context = {
    #     'is_realtor': profile.is_realtor,
    # }
    # return render(request, 'realtor_dashboard.html', context)
# logout page
def user_logout(request):
    #redireting back to the home page 
    logout(request)
    # messages.success(request, "Logged out successfully!")
    return redirect('login')

#@login_required(login_url='login/realtor/')
#changes begin 
def realtor_login(request):
    print('realtor login')
    # is_realtor = False
    # if request.user.is_authenticated: 
    #     is_realtor = request.user.groups.filter(name = "Realtors").exists()
    #return redirect('realtor_login')
#updating display of the home page 


#for customer 
#@login_required(login_url='login/customer/')
#changes begin 
def customer(request):
    is_customer = False
    if request.user.is_authenticated: 
        is_customer = request.user.groups.filter(name = "Customers").exists()
    return render(request, 'main/customer.html', {'is_customer' : is_customer})

# @login_required(login_url='login/customer/')
#changes begin 
def customer_login(request):
    is_customer = False
    if request.user.is_authenticated: 
        is_customer = request.user.groups.filter(name = "Customers").exists()
    return render(request, 'main/customer_login.html', {'is_customer' : is_customer})
#updating display of the home page 

def home_view(request):
    return render(request, 'home1.html')


#converting Flask chatbot to Django 
def chat(request):
    # items = ["Item 1", "Item 2", "Item 3"]
    return render(request, 'main/chat.html')

#to handle AJAX file 
@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('msg')
        # Here you can implement your logic to generate a response
        response_message = predict(user_message)
        print(response_message)
        return JsonResponse(response_message, safe=False)