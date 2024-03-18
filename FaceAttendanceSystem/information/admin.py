from django.contrib import admin
from .models import Subject, Student, SemToYear, SessionYear, Department
# from django.contrib.admin.models import LogEntry

# class LogEntryAdmin(admin.ModelAdmin):
#     # other configurations
#     list_display = ('__str__', 'user', 'action_time')

# admin.site.register(LogEntry, LogEntryAdmin)

# Register your models here.
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(SemToYear)
admin.site.register(SessionYear)
admin.site.register(Department)
