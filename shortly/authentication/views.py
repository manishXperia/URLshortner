from django.shortcuts import redirect, render
# import user modal to create functionality of user login and signup
from django.contrib.auth.models import User

from django.contrib import messages, auth

# Create your views here.

# handle the login authentication
def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            # check if userEmail and password are not empty
            if request.POST['userEmail'] and request.POST['password']:
                # check if userEmail exists and get the user objects
                try:
                    user  = User.objects.get(email = request.POST['userEmail'])
                    # if user found --> logged in 
                    auth.login(request, user)
                    # check if next param is in url
                    if request.POST['next'] is not None:
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('/')
                    return redirect('/')
                except User.DoesNotExist:
                    return render(request, 'login.html', { 'error': 'User Does not exists'})
            else:
                return render(request, 'login.html', { 'error': 'Please check empty fields'})
        else:
            return render(request, 'login.html')
    else:
        return redirect('/')


def signup(request):
    if request.method == "POST":
        #handle the signup, first check the password and confirm password are matched
        if request.POST['password'] == request.POST['confirm_password']:
            # check username, email and password not empty
            if request.POST['userName'] and request.POST['userEmail'] and request.POST['password']:
                # now create user and save information into database
                try:
                    # verify that: user already exists or not with userEmail
                    user = User.objects.get(email = request.POST['userEmail'])
                    return render(request, 'signup.html', { 'error': 'User Email already exists'})
                
                # if user not exists then create
                except User.DoesNotExist:
                    User.objects.create_user(
                        username = request.POST['userName'],
                        email  = request.POST['userEmail'],
                        password = request.POST['password']
                    )
                    messages.success(request, "User Registered Successfully!" )
                    return redirect(login)
            else:
                return render(request, 'signup.html', { 'error': 'Please check empty fields'})
        else:
            return render(request, 'signup.html', { 'error': 'Password does not match'})
        
    else:    
        return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/login')