from django.contrib import admin
from .models import Student, Audio, Attendance

class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "batch", "roll_no")
    list_filter = ("batch",)

class AudioAdmin(admin.ModelAdmin):
    list_display = ("student_roll", "audiofile")

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student_atnd", "date", "course", "teacher", "batch")
    list_filter = ("date", "teacher", "course")

admin.site.register(Student, StudentAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Attendance, AttendanceAdmin)