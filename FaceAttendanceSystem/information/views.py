from django.shortcuts import render
from .models import Subject, Student, SemToYear, SessionYear, Department
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import os

# Create your views here.
SEM = ["1st", "2nd", "3rd", "4th", "5th", "6th"]
YEAR = ["1st", "1st", "2nd", "2nd", "3rd", "3rd"]
DEPT = ["CST", "EE", "ME", "ETC"]



# @login_required
def Register(request):

    if len(SemToYear.objects.all()) == 0:
        for ob in zip(YEAR, SEM):
            SemToYear.objects.get_or_create(semester=ob[1], year=ob[0])
    if len(Department.objects.all()) == 0:
        for ob in DEPT:
            Department.objects.get_or_create(department=ob)
    data = {"Sem": SEM, "Dept": DEPT,}
    if request.method == "POST":
        try:
            photo = request.FILES["Photo"]
            sem = SemToYear.objects.filter(semester=request.POST["CurrentSemester"])[0]
            dep = Department.objects.filter(department=request.POST["Major"])[0]
            Student.objects.get_or_create(Photo=photo, RegID=request.POST["regid"], Name=request.POST["Name"], 
                                              DOB=request.POST["Birthday"], Gender=request.POST["Gender"], Major=dep, Sem=sem, 
                                              Phone=request.POST["PhoneNumber"], Email=request.POST["Email"])
            return render(request, "Register.html", data)
        except KeyError:
            data["warning"] = "Fill up form properly"
    return render(request, "Register.html", data)
    # return render(request, "login.html", data)


def Login(request):
    data={}
    if request.method=='POST':
        data['userid']=request.POST['userid']
        data['password']=request.POST['password']
        if request.POST['userid'] == '':
            data['warning1'] = 'Please fill User id'
        elif request.POST['password'] == '':
            data['warning2'] = 'Please fill password'
        # else:
        #     with connection.cursor() as c:
        #         c.execute("SELECT id FROM user where userid = %s and binary(password) = binary(%s)",[request.POST['userid'], request.POST['password']])
        #         d = c.fetchone()[0]
        #         if d is None:
        #             data['error']='No Data found'
        #             return render(request, 'login.html', data)
        #         else:
        #             request.session['user']=d
        #             return render(request, 'index.html', data)
    return render(request, 'login.html', data)