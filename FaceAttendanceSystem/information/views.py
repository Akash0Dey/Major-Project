from django.shortcuts import render, redirect
from .models import Subject, Student, SemToYear, SessionYear, Department
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
SEM = ["1st", "2nd", "3rd", "4th", "5th", "6th"]
YEAR = ["1st", "1st", "2nd", "2nd", "3rd", "3rd"]
DEPT = ["CST", "EE", "ME", "ETC"]



# @login_required
def register(request):

    if len(SemToYear.objects.all()) == 0:
        for ob in zip(YEAR, SEM):
            SemToYear.objects.get_or_create(semester=ob[1], year=ob[0])
    if len(Department.objects.all()) == 0:
        for ob in DEPT:
            Department.objects.get_or_create(department=ob)
    if request.method == "POST":
        data = {"Sem": SEM, "Dept": DEPT,
            "photo" : request.FILES["Photo"],
            "RegID":request.POST["regid"],
            "Name":request.POST["Name"],
            "DOB":request.POST["Birthday"],
            "Gender":request.POST["Gender"],
            "Phone":request.POST["PhoneNumber"],
            "Email":request.POST["Email"],
            "semester":request.POST["CurrentSemester"],
            "department":request.POST["Major"], 
        }
        try:
            user = request.user
            sem = SemToYear.objects.filter(semester=data["semester"])[0]
            dep = Department.objects.filter(department=data["department"])[0]
            Student.objects.get_or_create(user=user, Photo=data["photo"], RegID=request.POST["regid"], Name=request.POST["Name"], 
                                              DOB=request.POST["Birthday"], Gender=request.POST["Gender"], Major=dep, Sem=sem, 
                                              Phone=request.POST["PhoneNumber"], Email=request.POST["Email"])
            return render(request, "Register.html", data)
        except KeyError:
            data["warning"] = "Fill up form properly"
    else:
       
        data = {"Sem": SEM, "Dept": DEPT,
            "photo" : "",
            "RegID": "",
            "Name": "",
            "DOB": "",
            "Gender": "Male",
            "Phone": "",
            "Email": "",
            "semester": "1st",
            "department": "CST", 
        }
        return render(request, "Register.html", data)
    # return render(request, "login.html", data)


def signup(request):
    data={}
    if request.method=='POST':
        userid = request.POST['user']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        if userid == '':
            data['warning'] = 'Please fill User id'
        elif password == '':
            data['warning'] = 'Please fill password'
        elif password != repeatPassword : 
            data['warning'] = 'Both password don\'t match'

        else:
            if User.objects.filter(username=userid).exists():
                data["warning"] = "User Name already Exist"
            else:
                user = User.objects.create_user(username=userid, password=password)
                login(request, user)
            return redirect('register')
    return render(request, 'signup.html', data)


def Login(request):
    data={}
    if request.method=='POST':
        userid = request.POST['user']
        password = request.POST['password']
        if userid == '':
            data['warning'] = 'Please fill User id'
        elif password == '':
            data['warning'] = 'Please fill password'
        else:
            user = authenticate(request, username=userid, password=password)

        
            if user is None:
                data['warniing']='UserName or Password is wrong'
                return render(request, 'login.html', data)
            else:
                login(request, user)
                return redirect('register')
    return render(request, 'login.html', data)