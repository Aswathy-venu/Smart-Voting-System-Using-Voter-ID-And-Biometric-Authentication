from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
from adminapp . models import *
from panchayatapp . models import *
from django.http import HttpResponse
from Smart_Voting.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
import random
import string
from django.conf import settings



# Create your views here.
def uregister(request):
    if request.method=="POST":
        Firstname=request.POST.get("fname")
        Lastname=request.POST.get("lname")
        Address=request.POST.get("address")
        Gender=request.POST.get("gender")
        State=request.POST.get("state")
        District=request.POST.get("district")
        Panchayat=request.POST.get("panchayat")
        vid=request.POST.get("vid")
        DOB=request.POST.get("dob")
        Email=request.POST.get("email")
        password=request.POST.get("password")
        confirmpassword=request.POST.get("cpassword")
        img=request.FILES.get("img")

        if password==confirmpassword:
            if User_reg.objects.filter(Email= Email).exists():
                messages.info(request,'Email already exists')
        
            else:
                data=User_reg(Firstname=Firstname,Lastname= Lastname, Address=Address,Gender=Gender,
                            State= State,District=District,Panchayat=Panchayat,voterid=vid,DOB=DOB,Email=Email,
                            Password=password,img=img)
                data.save()
                return redirect("ulogin")
        else:
             messages.info(request,'password not match')
    return render(request,'User/uregister.html')





def ulogin(request):
    if request.method=="POST":
        try:
            email=request.POST.get('email')
            Password=request.POST.get('password')
            login=User_reg.objects.get(Email= email,Password= Password)
            request.session['email']=login.Email
            request.session['id']=login.id
            return redirect('uhome')
        except User_reg.DoesNotExist as e:
            messages.info(request,'Incorrect Password or Email')
    return render(request,'User/ulogin.html')


from . import PrepareDataset
from . PrepareDataset import *
def uhome(request):
    id=request.session['id']
    data=User_reg.objects.get(id=id)
    flag=data.flag
    time=time_set.objects.get(id=1)
   
    return render(request,"User/uhome.html",{'flag':flag,'time':time})
def uprofile(request):
    hid=request.session['id']
    prof=User_reg.objects.get(id=hid)
    return render(request,'User/uprofile.html', {'pro':prof})
def vote_verify1(request):
    cid=request.session['id']
    
    user_Obj=User_reg.objects.get(id=cid)
    Voterid=user_Obj.voterid
    if request.method == 'POST':
        Name=request.POST.get("name")
        VoterId=request.POST.get("vid")
        if Voterid == VoterId:
            return redirect(vote_verify2)

    
    return render(request,'User/vote1.html')

# def sendemail(request,id):
#     owner=jury.objects.get(id=id)
#     sub = forms.Subscribe()
#     if request.method == 'POST':
#         sub = request.POST['email']
#         name= request.POST['name']
#         subject = 'Hi, '+format(name) 
#         recepient = str(sub)
      
#         # get random password pf length 8 with letters, digits, and symbols
#         characters = string.ascii_letters + string.digits + string.punctuation
#         password = ''.join(random.choice(characters) for i in range(8))
#         jury.objects.filter(id=id).update(password=password)
        
#         message = '''Welcome to OurWorkGem site.
#         You can login with this password : ''' +format(password)
#         send_mail(subject, 
#             message, EMAIL_HOST_USER, [recepient], fail_silently = False)
#     return render(request,'projectadmin/sendmail.html',{"owner":owner})

def vote_verify2(request):
    id=request.session['id']
    user_Obj=User_reg.objects.get(id=id)
    Email = forms.Subscribe()
    name=user_Obj.Firstname
    email=user_Obj.Email
    if request.method == 'POST':
        Email=request.POST.get("email")
       
        if Email == email:
            recepient=email
            subject ="OTP"
            #get random password pf length 8 with letters, digits, and symbols
            characters = string.digits
            otp = ''.join(random.choice(characters) for i in range(4))
            User_reg.objects.filter(id=id).update(OTP=otp)
            
            message = '''Welcome to Plebiscite.
            The OTP for verification is : ''' +format(otp)
            send_mail(subject, 
                message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            return redirect(vote_verify4)

    
    return render(request,'User/vote2.html',{'owner':user_Obj})

def vote_verify4(request):
    cid=request.session['id']
    
    user_Obj=User_reg.objects.get(id=cid)
    OTP=user_Obj.OTP
    if request.method == 'POST':
        otp=request.POST.get("otp")
       
        if OTP == otp:
            return redirect(vote_verify3)

    
    return render(request,'User/vote4.html')
def vote_verify3(request):
    id=request.session['id']
    data=User_reg.objects.get(id=id)
    voteid=data.voteid
    pred=25

    if request.method=="POST":
        import numpy as np
        from . import PrepareDataset
        # from . PrepareDataset import *
        # import AddNewFace 
        import cv2
        import os
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        from sklearn.svm import SVC
        from sklearn.model_selection import GridSearchCV, KFold
        import pickle


        images = []
        labels = []
        labels_dic = {}

        # choice = input("Do you want to add new face? (Yes or No) ")
        # if choice == 'yes':
        #     AddNewFace.add_face()


        def collect_dataset():

            people = [person for person in os.listdir("people/")]

            for i, person in enumerate(people):
                labels_dic[i] = person
                for image in os.listdir("people/" + person):
                    if image.endswith('.jpg'):
                        images.append(cv2.imread("people/" + person + '/' + image, 0))
                        labels.append(i)
            return images, np.array(labels), labels_dic


        images, labels, labels_dic = collect_dataset()

        X_train = np.asarray(images)
        train = X_train.reshape(len(X_train), -1)

        sc = StandardScaler()
        X_train_sc = sc.fit_transform(train.astype(np.float64))
        pca1 = PCA(n_components=.97)
        new_train = pca1.fit_transform(X_train_sc)
        kf = KFold(n_splits=5,shuffle=True)
        param_grid = {'C': [.0001, .001, .01, .1, 1, 10]}
        gs_svc = GridSearchCV(SVC(kernel='linear', probability=True), param_grid=param_grid, cv=kf, scoring='accuracy')
        gs_svc.fit(new_train, labels)
        clf = gs_svc.best_estimator_
        filename = 'svc_linear_face.pkl'
        f = open(filename, 'wb')
        pickle.dump(clf, f)
        f.close()

        filename = 'svc_linear_face.pkl'
        svc1 = pickle.load(open(filename, 'rb'))

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.namedWindow("opencv_face ", cv2.WINDOW_AUTOSIZE)
        count=0
        bool=True
        while bool:
            ret, frame = cam.read()

            faces_coord = detect_face(frame)  # detect more than one face
            if len(faces_coord):
                faces = normalize_faces(frame, faces_coord)

                for i, face in enumerate(faces):  # for each detected face

                    t = face.reshape(1, -1)
                    t = sc.transform(t.astype(np.float64))
                    test = pca1.transform(t)
                    prob = svc1.predict_proba(test)
                    confidence = svc1.decision_function(test)
                    print(confidence)
                    print(prob)

                    pred = svc1.predict(test)
                    print(pred, pred[0])

                    name = labels_dic[pred[0]].capitalize()
                    print(name)
                    

                    cv2.putText(frame, name, (faces_coord[i][0], faces_coord[i][1] - 10),
                                cv2.FONT_HERSHEY_PLAIN, 2, (66, 53, 243), 2)

                draw_rectangle(frame, faces_coord)  # rectangle around face

            cv2.putText(frame, "ESC to exit", (5, frame.shape[0] - 5), cv2.FONT_HERSHEY_PLAIN, 1.3, (66, 53, 243), 2,
                        cv2.LINE_AA)

            cv2.imshow("opencv_face", frame)  # live feed in external
            if int(pred) == int(voteid):
                count=count+1
                print(count)
                print(voteid)
            if count>20:
                bool=False
                return redirect(viewcand)
            if cv2.waitKey(5) == 27:
                break
            

        cam.release()
        cv2.destroyAllWindows()
    return render(request,'User/vote3.html')




def uedit(request,id):
    edit=User_reg.objects.get(id=id)
    if request.method=="POST":
        edit.Firstname=request.POST.get('fname')
        edit.Lastname=request.POST.get('lname')
        edit.Address=request.POST.get('address')
        edit.Gender=request.POST.get('gender')
        edit.State=request.POST.get('state')
        edit.District=request.POST.get('district')
        edit.Panchayat=request.POST.get('Panchayat')
        edit.DOB=request.POST.get('dob')
        edit.Email=request.POST.get('email')
        edit.Password=request.POST.get('password')
        

        if len(request.FILES)!=0:
            
            edit.img=request.FILES.get('img')
            
            
            
        edit.save()
        return redirect("uprofile")

    return render(request,'User/uedit.html',{'pro':edit})



def viewcand(request):
    id=request.session['id']
    voters=User_reg.objects.get(id=id)
    vid=voters.voteid
    ppeople=panchayat_people.objects.get(voteID=vid)
    pid=ppeople.panchID
    # pid=
    vc=Candidates.objects.filter(panchID=pid)
    return render(request,'User/vcand.html',{'vc':vc})
def vote(request,id):
    cid=request.session['id']
    user=User_reg.objects.get(id=cid)
    Cand=Candidates.objects.get(id=id)
    count=Cand.VoteCount
    count=int(float(count))+1
    Candidates.objects.filter(id=id).update(VoteCount=count)
    User_reg.objects.filter(id=cid).update(flag=True)

    return redirect(uhome)
def uresult(request):
    candidates=Candidates.objects.all()
    max_rated_entry = Candidates.objects.latest('VoteCount')
    return render(request,"User/winner.html",{'win':max_rated_entry})


