from django.db import models

class Student(models.Model):
    name = models.CharField(null=False, max_length=50)
    batch = models.CharField(null=False, max_length=50)
    roll_no = models.IntegerField()

class Audio(models.Model):
    student_roll = models.IntegerField()
    val = models.IntegerField()
    #audiofile=models.FileField(upload_to="documents/")

class Attendance(models.Model):
    student_atnd = models.ForeignKey(Student, on_delete=models.CASCADE)
    date=models.DateTimeField()
    course=models.CharField(null=False,max_length=50)
    teacher=models.CharField(null=False,max_length=50)
    