from django.shortcuts import render, redirect
from .models import Subject, Student, SemToYear, SessionYear, Department
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

# Create your views here.
SEM = ["1st", "2nd", "3rd", "4th", "5th", "6th"]
YEAR = ["1st", "1st", "2nd", "2nd", "3rd", "3rd"]
DEPT = ["CST", "EE", "ME", "ETC"]


def home(request):
    data = {}
    if request.user.is_authenticated:
        data = {"register": Student.objects.filter(user=request.user).first()}
    return render(request, "index.html", data)

def profile(request):
    data = {}
    if request.user.is_authenticated:
        data = {"register": Student.objects.filter(user=request.user).first()}
    return render(request, "profile.html", data)

# def register(request):

#     # if semToYear and Department table don't exist create it

#     if len(SemToYear.objects.all()) == 0:
#         for ob in zip(YEAR, SEM):
#             SemToYear.objects.get_or_create(semester=ob[1], year=ob[0])
#     if len(Department.objects.all()) == 0:
#         for ob in DEPT:
#             Department.objects.get_or_create(department=ob)
#     user = request.user

#     # if Student exist

#     if Student.objects.filter(user=user).exists():
#         st = Student.objects.filter(user=user)[0]
#         data = {"Sem": SEM, "Dept": DEPT,
#             "RegID": st.RegID,
#             "Name": st.Name,
#             "DOB": st.DOB,
#             "Gender": st.Gender,
#             "Phone": st.Phone,
#             "Email": st.Email,
#             "semester": st.Sem.semester,
#             "department": st.Major.department,
#         }

#     if request.method == "POST":

#         # it is post method even when student existing mean they want to edit details

#         if Student.objects.filter(user=user).exists():
#             if request.POST["mode"] == "view":
#                 data["editmode"] = True
#                 return render(request, "Register.html", data)
            
#         # new student registering
            
#         data = {"Sem": SEM, "Dept": DEPT,
#             "Photo" : request.FILES["Photo"] if "Photo" in request.POST else st.Photo ,
#             "RegID":request.POST["regid"],
#             "Name":request.POST["Name"],
#             "DOB":request.POST["Birthday"],
#             "Gender":request.POST["Gender"],
#             "Phone":request.POST["PhoneNumber"],
#             "Email":request.POST["Email"],
#             "semester":request.POST["CurrentSemester"],
#             "department":request.POST["Major"], 
#         }
#         try:
#             sem = SemToYear.objects.filter(semester=data["semester"])[0]
#             dep = Department.objects.filter(department=data["department"])[0]
#             Student.objects.get_or_create(user=user, Photo= data["Photo"], RegID=request.POST["regid"], Name=request.POST["Name"], 
#                                               DOB=request.POST["Birthday"], Gender=request.POST["Gender"], Major=dep, Sem=sem, 
#                                               Phone=request.POST["PhoneNumber"], Email=request.POST["Email"])
#             return redirect("home")  # Redirect
#         except KeyError:
#             data["warning"] = "Fill up form properly"
#         return render(request, "Register.html", data)  # Redirect
#     else:
#         if Student.objects.filter(user=user).exists():
#             data["viewmode"] = True
#         else:
#             data = {"Sem": SEM, "Dept": DEPT,
#                 "RegID": "",
#                 "Name": "",
#                 "DOB": "",
#                 "Gender": "Male",
#                 "Phone": "",
#                 "Email": "",
#                 "semester": "1st",
#                 "department": "CST", 
#             }
#         return render(request, "Register.html", data)
    # return render(request, "login.html", data)

def register(request):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return redirect('login') # Redirect to login page if user is not authenticated

    # Check if necessary tables exist and create them if not
    if SemToYear.objects.count() == 0:
        for year, semester in zip(YEAR, SEM):
            SemToYear.objects.create(year=year, semester=semester)
    if Department.objects.count() == 0:
        for dept in DEPT:
            Department.objects.create(department=dept)


    # Check if student already exists for the user
    student = Student.objects.filter(user=request.user).first()

    if request.method == "POST":
        form_data = request.POST
        form_files = request.FILES

        # Handle editing existing student details
        if student and form_data.get("mode") == "view":
            data = {
                "Sem": SEM,
                "Dept": DEPT,
                "editmode": True,
                "RegID": student.RegID,
                "Name": student.Name,
                "DOB": student.DOB,
                "Gender": student.Gender,
                "Phone": student.Phone,
                "Email": student.Email,
                "semester": student.Sem.semester,
                "department": student.Major.department,
            }
            return render(request, "register.html", data)

        # Handle new student registration or updating existing details
        try:
            sem = SemToYear.objects.get(semester=form_data["CurrentSemester"])
            dep = Department.objects.get(department=form_data["Major"])


            # If student already exists, update the details
            if student:
                photo = form_files.get("Photo")
                student.Photo =photo if photo else student.Photo
                student.RegID = form_data["regid"]
                student.Name = form_data["Name"]
                student.DOB = form_data["Birthday"]
                student.Gender = form_data["Gender"]
                student.Major = dep
                student.Sem = sem
                student.Phone = form_data["PhoneNumber"]
                student.Email = form_data["Email"]
                student.save()
            else:
                # Otherwise, create a new student record
                Student.objects.create(
                    user=request.user,
                    Photo=form_files.get("Photo"),
                    RegID=form_data["regid"],
                    Name=form_data["Name"],
                    DOB=form_data["Birthday"],
                    Gender=form_data["Gender"],
                    Major=dep,
                    Sem=sem,
                    Phone=form_data["PhoneNumber"],
                    Email=form_data["Email"],
                )
            
            return redirect("home")  # Redirect to home page after successful registration/update
        except KeyError:
            data = {"warning": "Fill up the form properly"}

    else:
        data = {
            "Sem": SEM,
            "Dept": DEPT,
            "photo": student.Photo.url if student else "",
            "RegID": student.RegID if student else "",
            "Name": student.Name if student else "",
            "DOB": student.DOB if student else "",
            "Gender": student.Gender if student else "Male",
            "Phone": student.Phone if student else "",
            "Email": student.Email if student else "",
            "semester": student.Sem.semester if student else "1st",
            "department": student.Major.department if student else "CST",
            "viewmode": bool(student),
        }
    return render(request, "register.html", data)

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
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
                # user = authenticate(request, username=userid, password=password)
                login(request, user)
                request.session.set_expiry(0)
                return redirect('register')
    return render(request, 'signup.html', data)


def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
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
                request.session.set_expiry(0)
                return redirect('register')
    return render(request, 'login.html', data)

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")