from information.models import database
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","FaceAttendanceSystem.settings")

import django
django.setup()


database()