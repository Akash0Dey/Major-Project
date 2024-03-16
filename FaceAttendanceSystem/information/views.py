from django.shortcuts import render
from .models import Subject, Student, SemToYear, SessionYear, Department
from django.db import models
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
SEM = ["1st", "2nd", "3rd", "4th", "5th", "6th"]
YEAR = ["1st", "1st", "2nd", "2nd", "3rd", "3rd"]
DEPT = ["CST", "EE", "ME", "ETC"]

def Register(request):
    # database()
    if len(SemToYear.objects.all()) == 0:
        for ob in zip(YEAR, SEM):
            SemToYear.objects.get_or_create(semester=ob[1], year=ob[0])
    if len(Department.objects.all()) == 0:
        for ob in DEPT:
            Department.objects.get_or_create(department=ob)
    data = {"Sem": SEM, "Dept": DEPT,}
    # if request.session.has_key('user'):
    if request.method == "POST":
        try:
            photo = request.FILES["Photo"]
            # Save the uploaded file with a new name based on RegID
            fs = FileSystemStorage()
            filename = f"{request.POST['regid']}.{photo.name.split('.')[-1]}"
            file_path = fs.save(os.path.join("Student", filename), photo)
            sem = SemToYear.objects.filter(semester=request.POST["CurrentSemester"])[0]
            dep = Department.objects.filter(department=request.POST["Major"])[0]
            S = Student.objects.get_or_create(Photo=file_path, RegID=request.POST["regid"], Name=request.POST["Name"], 
                                              DOB=request.POST["Birthday"], Gender=request.POST["Gender"], Major=dep, Sem=sem, 
                                              Phone=request.POST["PhoneNumber"], Email=request.POST["Email"])
            return render(request, "Register.html", data)
        except KeyError:
            data["warning"] = "Fill up form properly"
    return render(request, "Register.html", data)
    # return render(request, "login.html", data)


# Department.objects.get_or_create("CST")
# SemToYear.objects.get_or_create(semester="3rd", year="2nd")

def database():
    Dept = ["CST", "EE", "ETC", "ME"]
    sem = {"1st":"1st", "2nd":"1st", "3rd":"2nd", "4th":"2nd", "5th":"3rd", "6th":"3rd"}
    dep =  Department.objects.all()
    print(dep)
    for d in Dept:
        Department.objects.get_or_create(d).save()
    for s in sem:
        SemToYear.objects.get_or_create(s, sem[s]).save()