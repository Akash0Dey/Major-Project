from django.urls import path
from . import views

urlpatterns = [
    # path('Student/', include("Data.urls"), name="Student"),
    # path('Teacher/', include("Data.urls"), name="Teacher"),
    # path('Routine/', include("Data.urls"), name="Routine"),
    # path('/', include("Data.urls"), name="index"),
    # path('Attendance/', include("Attendance.urls"), name="Attendance"),
    # path('Past Class/', include("PastClass.urls"), name="PastClass"),
    path('register/', views.register, name="register"),
    path('login/', views.Login, name="login"),
    path('signup/', views.signup, name="signup"),
]