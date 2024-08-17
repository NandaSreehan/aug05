from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app1.models import tweet

# Create your views here.
def home(request):
    objs=tweet.objects.all()[::-1]
    return render(request,'index.html',{'result':objs})


def loginV(request):
    if request.user.is_authenticated:
        messages.warning(request,"Mama you already logged! ")
        return redirect('homepage')
    #logout(request)
    if request.method=="POST":
        a=request.POST.get('ip1')
        b=request.POST.get('ip2')
        result=authenticate(request,username=a,password=b)
        if result is not None:
            print(a,b,type(result))
            login(request,result)
            messages.success(request,"Thank you for coming back ! ")
            return redirect('profilepage')
        else:
            messages.error(request,"are you trying to cheat me ! Wrong creds")
            return redirect('loginpage')
    return render(request,'login.html')

@login_required(login_url='loginpage')
def profile(request):
    if request.user.is_superuser:
        print(request.user.username)
        return redirect('/admin')

    return render(request,'profile.html')


def register(request):
    if request.user.is_authenticated:
        messages.warning(request,"Man you already have an account !")
        return redirect('homepage')
        
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        passw=request.POST.get('passw')
        cpass=request.POST.get('cpass')
        email=request.POST.get('email')
        uname=request.POST.get('uname')
        print(fname,lname,passw,cpass,email,uname)

        #validation username
        if User.objects.filter(username=uname).exists():
            messages.error(request,"Username already exists !")
            return redirect('loginpage')
        #validation for password
        if len(passw)<8:
            messages.error(request,"Password must be 8 chars")
            return redirect('registerpage')
        #validation for cpass
        if (cpass!=passw):
            messages.error(request,"Passwords doest match")
            return redirect('registerpage')
        
        obj=User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=email,password=passw)
        obj.save()
        messages.success(request,"Hey your account is ready, Login now")
        return redirect('loginpage')

    return render(request,'register.html')




@login_required(login_url='loginpage')
def tweetView(request):
    if request.method=="POST":
        a=request.POST.get('post')
        u=str(request.user.username)
        obj=tweet(uname=u,post=a)
        obj.save()
    return render(request,'tweet.html')

def display(request,rid):
    b=tweet.objects.get(id=rid)
    if request.method=="POST":
        b.post=request.POST.get('desc')
        b.save()
    return render(request,'single.html',{'res':b})


@login_required(login_url='loginpage')
def deleteView(request,rid):
    if request.user.is_superuser:
        obj=tweet.objects.get(id=rid)
        obj.delete()
        messages.success(request,"Epudu santhoshama, Deleted successfully")
        return redirect('homepage')
    else:
        messages.warning(request,"nanu mosam cheyalevu, you are not admin")
        return redirect('homepage')



def logoutV(request):
    logout(request)
    messages.info(request,"are you leaving me ! you cheat")
    return redirect('loginpage')
