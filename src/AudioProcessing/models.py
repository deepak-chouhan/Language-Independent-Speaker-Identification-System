from django.db import models

class Student(models.Model):
    name = models.CharField(null=False, max_length=50)
    batch = models.CharField(null=False, max_length=50)
    roll_no = models.IntegerField()
