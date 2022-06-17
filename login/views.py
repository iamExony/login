from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pword = request.POST['pword']
        cpword = request.POST['cpword']

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exist, please try another")
            return redirect('signup')

        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email Already Exist, please try another")
            return redirect('signup')

        if pword != cpword:
            messages.error(request, "Password does not match")
            return redirect('signup')


        myuser = User.objects.create_user(username, email, pword)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been successfully created.")
        
        return redirect('signin')
    return render(request, 'login/signup.html')
    

def signin(request):
        if request.method == 'POST':
            username = request.POST['username']
            pword = request.POST['pword']


            user = authenticate(username=username, password=pword)

            if user is not None:
                login(request, user)
                fname = user.first_name
                messages.success(request, "Your Account have successfully Logged in")
                return render(request, "login/index.html", {'fname': fname})
                
    
            else:
                messages.error(request, "Invalid Username or password")
                return redirect(request, 'index')
        return render(request, 'login/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully")
    return redirect('index')
