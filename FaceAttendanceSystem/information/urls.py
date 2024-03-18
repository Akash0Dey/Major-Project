from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # path('Student/', include("Data.urls"), name="Student"),
    # path('Teacher/', include("Data.urls"), name="Teacher"),
    # path('Routine/', include("Data.urls"), name="Routine"),
    # path('/', include("Data.urls"), name="index"),
    # path('Attendance/', include("Attendance.urls"), name="Attendance"),
    # path('Past Class/', include("PastClass.urls"), name="PastClass"),
    path('Register/', views.Register, name="Register"),
    path('login/', views.Login, name="Login"),
]