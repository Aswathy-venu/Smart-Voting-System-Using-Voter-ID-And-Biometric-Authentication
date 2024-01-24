from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
from userapp.models import *
import cv2
import os
# from . import AddNewFace
from . import PrepareDataset
from . PrepareDataset import *
from django.http import HttpResponse

# Create your views here.
# Create your views here.
def pregister(request):
    if request.method=="POST":
        Firstname=request.POST.get("fn")
        Lastname=request.POST.get("ln")
        Pid=request.POST.get("pi")
        Address=request.POST.get("add")
        Pname=request.POST.get("pn")
        Email=request.POST.get("ei")
        password=request.POST.get("pass")
        confirmpassword=request.POST.get("cpass")
        img=request.FILES.get("img")

        if password==confirmpassword:
            if panchayat_reg.objects.filter(Email= Email).exists():
                messages.info(request,'Email already exists')
        
            else:
                data=panchayat_reg(Firstname=Firstname,Lastname= Lastname,Pid=Pid,
                               Address=Address,Pname=Pname,Email=Email,
                            Password=password,img=img)
                data.save()
                return redirect("plogin")
        else:
             messages.info(request,'password not match')
    return render(request,'panchayat/pregister.html')

def plogin(request):
    if request.method=="POST":
        try:
            pid=request.POST.get('pid')
            Password=request.POST.get('pass')
            login=panchayat_reg.objects.get(Pid=pid,Password=Password)
            request.session['Firstname']=login.Firstname
            request.session['id']=login.id
            return redirect('phome')
        except panchayat_reg.DoesNotExist as e:
            messages.info(request,'Incorrect Password or Email')
    return render(request,'panchayat/plogin.html')

def phome(request):
    
    # return HttpResponse("Hello World!")
    return render(request,"panchayat/phome.html")

def plist(request):
    pt=panchayat_people.objects.all()
    return render(request,"panchayat/plist.html",{'pt':pt})

def pupdate(request,id):

    pt=panchayat_people.objects.get(id=id)
    Name=pt.Name
    if request.method=="POST":
        voteID=request.POST.get("voteID")

        panchayat_people.objects.filter(id=id).update(voteID=voteID)
        User_reg.objects.filter(Firstname=Name).update(voteid=voteID)

        return redirect('phome')
    return render(request,"panchayat/pupdate.html",{'pt':pt})

def addcand(request):
    if request.method=="POST":
        Name=request.POST.get("Name")
        Party=request.POST.get("Party")
        panchID=request.session['id']
        electionsymbol=request.FILES.get("electionsymbol")
        # VoteCount=request.POST.get("VoteCount")
        data=Candidates(Name=Name,Party= Party,panchID_id=panchID,
                               electionsymbol=electionsymbol)
        data.save()
        return redirect("phome")
    
    return render(request,'panchayat/addcand.html')



def pprofile(request):
    hid=request.session['id']
    prof=panchayat_reg.objects.get(id=hid)
    return render(request,'panchayat/pprofile.html',{'pro':prof})


def pform(request):
    global Name
    
    choice = 'yes'
    if request.method=="POST":
        Name=request.POST.get("Name")
        panchID=request.session['id']
        pf=panchayat_people(Name=Name,panchID_id=panchID)
        pf.save()
        
        if choice == 'yes':
            # AddNewFace.add_face(Name)
            cam = cv2.VideoCapture(0)

    # folder = "people/" + input('Person:').lower()
            folder = "people/" + Name.lower()

            try:
                os.mkdir(folder)

                flag_start_capturing = False
                sample = 1
                cv2.namedWindow("Face", cv2.WINDOW_AUTOSIZE)

                while True:
                    ret, frame = cam.read()

                    # faces_coord = detect_face(frame)
                    if frame.ndim != 2:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    detector = cv2.CascadeClassifier("xml/frontal_face.xml")
                    faces = detector.detectMultiScale(frame, 1.2, 5)

                         
                    faces_coord=faces

                    if len(faces_coord):
                        faces = normalize_faces(frame, faces_coord)
                        cv2.imwrite(folder + '/' + str(sample) + '.jpg', faces[0])

                            # if flag_start_capturing:
                        sample += 1

                    draw_rectangle(frame, faces_coord)
                    cv2.imshow('Face', frame)
                    keypress = cv2.waitKey(1)

                    if keypress == ord('c'):

                        if not flag_start_capturing:
                            flag_start_capturing = True

                    if sample > 150:
                        break

                cam.release()
                cv2.destroyAllWindows()
            except FileExistsError:
                print("Already exists")


    return render(request,'panchayat/pform.html')


def pedit(request,id):
    edit=panchayat_reg.objects.get(id=id)
    if request.method=="POST":

        if len(request.FILES)!=0:
            edit.Firstname=request.FILES.get('fn')
            edit.Lastname=request.FILES.get('ln')
            edit.Pid=request.FILES.get('pi')
            edit.Address=request.FILES.get('add')
            edit.Pname=request.FILES.get('pn')
            edit.Email=request.FILES.get('ei')
            edit.Password=request.FILES.get('pass')
            edit.confirmPassword=request.FILES.get('cpassword')
            if len(request.FILES)!=0:
                edit.img=request.FILES.get('img')
            edit.save()
        return redirect("pprofile")
    return render(request,'panchayat/pedit.html',{'pro' :edit})




def pedit(request,id):
    edit=panchayat_reg.objects.get(id=id)
    if request.method=="POST":
        edit.Firstname=request.POST.get('fn')
        edit.Lastname=request.POST.get('ln')
        edit.Pid=request.POST.get('pi')
        edit.Address=request.POST.get('add')
        edit.Pname=request.POST.get('pn')
        edit.Email=request.POST.get('ei')
        edit.Password=request.POST.get('pass')
        

        if len(request.FILES)!=0:
            
            edit.img=request.FILES.get('img')
            
            
            
        edit.save()
        return redirect("pprofile")

    return render(request,'panchayat/pedit.html',{'pro':edit})


def winner(request):
    id=request.session['id']
    candidates=Candidates.objects.all()
    max_rated_entry = Candidates.objects.latest('VoteCount')



    return render(request,'panchayat/winner.html',{'win':max_rated_entry})

