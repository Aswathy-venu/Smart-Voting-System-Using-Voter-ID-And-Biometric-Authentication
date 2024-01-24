from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
from django.http import HttpResponse
from panchayatapp.models import *
from userapp.models import *
# from panchayatapp.models import *



def ahome(request):
     return render(request,"admin/ahome.html")
def tables(request):
     candidates=Candidates.objects.all()
     User=User_reg.objects.all()
     people=panchayat_people.objects.all()
     panchayat=panchayat_reg.objects.all()

     return render(request,"admin/tables.html",{'cand':candidates,'user':User,'people':people,'panchayat':panchayat})


# Create your views here.
def aregister(request):
    if request.method=="POST":
        Firstname=request.POST.get("fname")
        Lastname=request.POST.get("lname")
        Address=request.POST.get("address")
        DOB=request.POST.get("dob")
        Email=request.POST.get("email")
        password=request.POST.get("password")
        confirmpassword=request.POST.get("cpassword")
        img=request.FILES.get("img")

        if password==confirmpassword:
            if admin_reg.objects.filter(Email= Email).exists():
                messages.info(request,'Email already exists')
        
            else:
                data=admin_reg(Firstname=Firstname,Lastname= Lastname, Address=Address,DOB=DOB,Email=Email,
                            Password=password,img=img)
                data.save()
                return redirect("alogin")
        else:
             messages.info(request,'password not match')
    return render(request,'admin/aregister.html')





def alogin(request):
    if request.method=="POST":
        try:
            email=request.POST.get('email')
            Password=request.POST.get('password')
            login=admin_reg.objects.get(Email= email,Password= Password)
            request.session['email']=login.Email
            request.session['id']=login.id
            return redirect('index')
        except admin_reg.DoesNotExist as e:
            messages.info(request,'Incorrect Password or Email')
    return render(request,'admin/alogin.html')




def index(request):
    # return HttpResponse("Hello World!")
    return render(request,"admin/index.html")

def result(request):
    candidates=Candidates.objects.all()
    max_rated_entry = Candidates.objects.latest('VoteCount')
    return render(request,"admin/result.html",{'data':max_rated_entry})

def capprove(request,id):
    Candidates.objects.filter(id=id).update(approve=True)
    Candidates.objects.filter(id=id).update(Reject=False)

    return redirect('tables')

def creject(request,id):
    Candidates.objects.filter(id=id).update(Reject=True)
    Candidates.objects.filter(id=id).update(approve=False)

    return redirect('tables')
def cresult(request,id):
    candidates=Candidates.objects.filter(id=id).update(result=True)
    # max_rated_entry = Candidates.objects.latest('VoteCount')
    

    return redirect('tables')

def start(request):
    time_set.objects.filter(id=1).update(start=True)
    time_set.objects.filter(id=1).update(end=False)

    
    # max_rated_entry = Candidates.objects.latest('VoteCount')
    

    return redirect('tables')
def end(request):
    time_set.objects.filter(id=1).update(end=True)
    time_set.objects.filter(id=1).update(start=False)

    
    # candidates.save()
    # max_rated_entry = Candidates.objects.latest('VoteCount')
    

    return redirect('tables')