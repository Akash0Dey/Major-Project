import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
from datetime import datetime
import time


cred = credentials.Certificate("face-recognition.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://face-recognition-attenda-be560-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "face-recognition-attenda-be560.appspot.com",
})

major = ["CST", "ME", "ETC", "EE"]
sem = ["1st", "2nd", "3rd", "4th", "5th", "6th"]


def ref(reference: str):
    return db.reference(reference)


def teacherTeachSub(teacher, sub, year, semester, major):
    teach = ref(f"Teachers/{year}/{teacher}/{major}/{semester}/{sub}")
    if teach.get() is None:
        teach = ref(f"Teachers/{year}/{teacher}")
        try:
            temp = teach.get().keys()
        except AttributeError:
            teach.set({
                "CST": "None",
                "ME": "None",
                "ETC": "None",
                "EE": "None",
            })
        teach = ref(f"Teachers/{year}/{teacher}/{major}")
        try:
            temp = teach.get().keys()
        except AttributeError:
            teach.set({
                "1st": "None",
                "2nd": "None",
                "3rd": "None",
                "4th": "None",
                "5th": "None",
                "6th": "None",
            })
        teach = ref(f"Teachers/{year}/{teacher}/{major}/{semester}/{sub}").set({
            "Total Attendance": 0,
        })
        return False
    return True


def newSubject(name, semester, teacher):
    sub = ref(f"Subjects/{semester}").get()
    if "None" == sub:
        sub = {}
    sub[name] = teacher
    ref(f"Subjects/{semester}").set(sub)


def newStudent(name, reg_id, major, current_year, semester, dob, gender,
               email, phone, attendance="None", last_attendance="None"):
    ref(f"Students/{reg_id}").set({
        "Name": name,
        "Major": major,
        "Current semester": semester,
        "Current Year": current_year,
        "Date of Birth": dob,
        "Email": email,
        "Phone no": phone,
        "Gender": gender,
        "Last Attendance": last_attendance,
        "Attendance": attendance
    })


def Attendance(teacher, sub, year, semester, major, mode, value=1):
    if mode == 0:
        stud = ref(f"Students").get()
        student = {}
        for key, value in zip(stud.keys(), stud.values()):
            # print(key, value["Major"], value["Current semester"])
            if (value["Major"] == major) & (value["Current semester"] == semester):
                student[key] = value
        data = {reg: 0 for reg in student.keys()}
        date_time = str(datetime.now()).split(" ")
        ref(f"Attendance").set({
            sub: data,
            "Date": date_time[0],
            "Time": ":".join(date_time[1].split(":")[:2]),
        })
        # ref(f"Attendance/{sub}")
    elif mode == 1:
        attend = ref(f"Attendance/{sub}").get()
        attended = {key: value for key, value in zip(attend.keys(), attend.values()) if value != 0}
        date = ref(f"Attendance/Date").get()
        time = f"{ref(f'Attendance/Time').get()} {':'.join(str(datetime.now()).split(' ')[1].split(':')[:2])}"
        ref(f"Year/{year}/{major}/{semester}/{date}/{time}").set({
            "Subject": sub,
            "Teacher": teacher,
            "Attended": len(attended),
        })
        ref(f"Teachers/{year}/{teacher}/{major}/Past Class/{date}/{time}").set({
            "Subject": sub,
            "Attended": len(attended),
        })
        teach = ref(f"Teachers/{year}/{teacher}/{major}/{semester}/{sub}")
        try:
            info = teach.get()
            info = {key: value for key, value in zip(info.keys(), info.values())}
            info["Total Attendance"] += value
        except AttributeError:
            info = {"Total Attendance": value}
        for one in attended:
            try:
                info[one] = info[one] + attended[one]
            except:
                info[one] = attended[one]

            at = ref(f"Students/{one}/Attendance/{sub}").get()
            at = 0 if at is None else at
            at += attended[one]
            ref(f"Students/{one}/Attendance/{sub}").set(at)
        teach.set(info)
        ref("Attendance").delete()


def oneAttendance(student_id, sub, mode=0, value=1):
    try:
        if mode == 0:
            ref(f"Attendance/{sub}/{student_id}").set(value)
        elif mode == 1:
            ref(f"Attendance/{sub}/{student_id}").set(0)
        return True
    except FileNotFoundError:
        return False


class FirebaseDatabase:

    def __init__(self, year="2023-24"):
        self.Year = year
        self.checkingYear()

    # Checking If The Year is Already Exist in Database

    def checkingYear(self):
        try:
            year = ref("Year").get().keys()
            if self.Year not in year:
                self.databaseCreate()
        except AttributeError:
            self.databaseCreate()

    def databaseCreate(self):

        # year database create

        year = [f'Year/{self.Year}/{m}' for m in major]
        for x in year:
            s = [f'{x}/{y}' for y in sem]
            for z in s:
                ref(z).set("Date")

        # Subjects database create
        for z in sem:
            ref(f"Subjects/{z}").set("None")

        # Student database create

        ref("Students").set("None")

        # Teacher database create

        ref(f"Teachers/{self.Year}").set("None")


# class Register:
#     def __init__(self, name, major, year, starting_year, ):
#         self.name = name


if __name__ == "__main__":
    # db.reference("/").delete()
    F = FirebaseDatabase()
    # newSubject("python", "3rd", "SH")
    # newSubject("c", "3rd", "FM")
    # newStudent("Akash Dey", "D212204363", "CST", "3rd", "5th", "akadey@ga.com", {"Python": 2})
    # newStudent("Bikash Dey", "D212204366", "ME", "3rd", "5th", "akadey@ga.com", {"C": 2})
    # newStudent("Sayan Paul", "D212204368", "CST", "3rd", "5th", "akadey@ga.com", {"C": 2})
    # teacherTeachSub("FM", "C", "2023-24", "3rd", "CST")
    # teacherTeachSub("FM", "Python", "2023-24", "3rd", "CST")
    # Attendance("FM", "Python", "2023-24", "5th", "CST", 0, 2)
    # time.sleep(60)
    # oneAttendance("D212204363", "Python", value=2)
    # oneAttendance("D212204368", "Python", value=2)
    # Attendance("FM", "Python", "2023-24", "5th", "CST", 1, 2)
    # Attendance("FM", "C", "2023-24", "5th", "CST", 0, 2)
    # time.sleep(60)
    # oneAttendance("D212204363", "C", value=2)
    # oneAttendance("D212204368", "C", value=2)
    # Attendance("FM", "C", "2023-24", "5th", "CST", 1, 2)
