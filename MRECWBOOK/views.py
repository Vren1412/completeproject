from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import UserRegistrationModel,BookModel

def index(request):
    data = BookModel.objects.all()
    return render(request, 'index.html', {'data':data})

def base(request):
    return render(request, 'base.html', {})

def AdminLogin(request):
    return render(request, 'AdminLogin.html', {})

def UserLogin(request):
    return render(request, 'UserLogin.html', {})

def UserRegister(request):
    return render(request, 'UserRegister.html', {})

def logout(request):
    return  redirect('index') 



def UserLoginAction(request):
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')

        try:
            user = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            if user.status == "Approved":
                request.session['userid'] = user.id
                request.session['username'] = user.name
                messages.success(request, f"Welcome {user.name}!")
                return redirect('UserHome')
            else:
                messages.error(request, "Your account is not approved yet.")
        except UserRegistrationModel.DoesNotExist:
            messages.error(request, "Invalid Login ID or Password.")

    return render(request, 'UserLogin.html')


def UserRegisterAction(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        locality = request.POST.get('locality')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')

        if UserRegistrationModel.objects.filter(loginid=loginid).exists():
            messages.error(request, 'Login ID already exists.')
            return render(request, 'UserRegister.html')

        if UserRegistrationModel.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'UserRegister.html')

        UserRegistrationModel.objects.create(
            name=name,
            loginid=loginid,
            password=password,  
            mobile=mobile,
            email=email,
            locality=locality,
            address=address,
            city=city,
            state=state,
            status='Pending' 
        )

        messages.success(request, 'Registration successful! Please wait for admin approval.')
        return redirect('UserRegister') 

    return render(request, 'UserRegister.html')

 

def AdminLoginActions(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'Admin' and pswd == 'Admin':
            return render(request, 'admins/AdminHome.html')

        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})