"""
URL configuration for FaceAttendanceSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from information import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('Student/', include("Data.urls"), name="Student"),
    # path('Teacher/', include("Data.urls"), name="Teacher"),
    # path('Routine/', include("Data.urls"), name="Routine"),
    # path('/', include("Data.urls"), name="index"
    # path('Attendance/', include("Attendance.urls"), name="Attendance"),
    # path('Past Class/', include("PastClass.urls"), name="PastClass"),
    path('', include("information.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
