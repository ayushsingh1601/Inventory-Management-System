from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import re
# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('/')
def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')

    else:
        return render(request,'login.html')
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        ff=0
        while True:   
            if not re.search("[@]", email): 
                messages.info(request,'Not a valid Email-id')
                ff=-1
                return redirect('register')
                break
            else:
                ff=0
                break
        
        password = password1
        flag = 0
        while True:   
            if (len(password)<8): 
                flag = -1
                messages.info(request,'Password length must be at least 8 characters.NOTE: Password must contain at least one capital alphabet,special character and numeric digit.')
                return redirect('register')
                break
            elif not re.search("[A-Z]", password): 
                flag = -1
                messages.info(request,'Password must contain atleast one capital alphabet.NOTE:Password must contain at least one capital alphabet,special character and numeric digit.')
                return redirect('register')
                break
            elif not re.search("[0-9]", password): 
                flag = -1
                messages.info(request,'Password must contain atleast one numeric digit. NOTE:Password must contain at least one capital alphabet,special character and numeric digit.')
                return redirect('register')
                break
            elif not re.search("[!@#$%^&*()_]", password): 
                flag = -1
                messages.info(request,'Password must contain atleast one special character.Password must contain at least one capital alphabet,special character and numeric digit.')
                return redirect('register')
                break
            elif re.search("\s", password): 
                flag = -1
                break
            else: 
                flag = 0
                break
  
    
   

        if password1==password2 and flag == 0 and ff==0:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already registered')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1 , email=email, first_name=first_name, last_name=last_name)
                user.save()
                print("usr don")
                return redirect('login')
        else:
            messages.info(request,'Password not matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'register.html')