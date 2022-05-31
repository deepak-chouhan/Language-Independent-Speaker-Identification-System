import os
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
import base64
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from .helper import *

def my_view(request):
    cur_user = request.user
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            print("none")
    return render(request, "AudioProcessing/login.html")

@login_required()
def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect("/login")
    return render(request, "AudioProcessing/logout.html")
    
@login_required()
def record(request):
    return render(request, "AudioProcessing/index.html")

def dashboard(request):
    cur_user = request.user
    if request.method == "POST":
        course = request.POST["course"]
        batch = request.POST["batch"]
        date = request.POST["date"]

        dates = Attendance.objects.filter(course=course, date__contains=date, batch=batch.upper())
        print(dates)


        file = open("filename.csv", "w")
        file.truncate()
        writer = csv.writer(file)

        head2=['Name','roll','date']
        writer.writerow(head2)
        for i in dates:
            date=[i.student_atnd.name, i.student_atnd.roll_no, i.date]
            print(date)
            writer.writerow(date)
        file.close()

        file_path = "filename.csv"
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + f"{batch}_{course}.csv"
            return response

    return render(request, "AudioProcessing/dashboard.html")

@csrf_exempt
def save(request):
    curuser=request.user;
    if request.method == "POST":

        # details
        course = request.POST["course"]
        batch = request.POST["batch"]
        teacher = request.POST["teacher"]

        # array of base64 string
        audio = request.POST["audio"]
        audio = audio.split(",")[1]

        path = "./media/new_file.wav"
        audio_data = base64.urlsafe_b64decode(audio)

        # # saving the file
        audio_file = open(path, 'wb')
        audio_file.write(audio_data)

        # predicting student
        roll = predict_speaker(path)
        print(roll)

        student = Student.objects.filter(roll_no=roll[0])
        print(student)
        attendence_obj = Attendance.objects.create(student_atnd=student[0], teacher=str(teacher), course=course, batch=batch.upper())
        attendence_obj.save()

        return JsonResponse({"response": "Attendence Marked", "res": str(roll[0])})

@csrf_exempt          
def Student_reg(request):
    if request.method=="POST":

        # array of base64 string
        audios = request.POST.getlist("audio[]")
        name=(request.POST.getlist("name")[0])
        batch=request.POST.getlist("batch")[0]
        rollno=request.POST.getlist("roll_no")[0]
        newstudent=Student.objects.create(name=name, batch=batch, roll_no=rollno)
        newstudent.save()
        i = 0
        
        for audio in audios:

            audio_data=base64.b64decode(audio)

            # saves the file in <student_id>__<roll_no>__<name>__<file_number>.mp3 format
            string1="newsrc/" + str(newstudent.id) + "__" + str(rollno)+ "__" + str(name) + "__" + str(i) + '.wav'
            i += 1
            print(string1)

            # saving the file
            with open(string1,'wb') as aud:
                aud.write(audio_data)
            audioobj = Audio.objects.create(student_roll=rollno, audiofile=string1)
            audioobj.save
    return render(request,"AudioProcessing/student.html")

