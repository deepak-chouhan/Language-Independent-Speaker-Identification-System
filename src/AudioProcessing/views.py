from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from requests import patch
from .forms import *
import base64
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

from .helper import *

def my_view(request):
    cur_user = request.user
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/rec")
            
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
    return render(request, "AudioProcessing/dashboard.html")

@csrf_exempt
def save(request):
    curuser=request.user;
    if request.method == "POST":

        # details
        # course = request.POST["course"]
        # batch = request.POST["batch"]
        # teacher = request.POST["teacher"]

        # array of base64 string
        audio = request.POST["audio"]
        audio = audio.split(",")[1]

        path = "./media/new_file.wav"
        audio_data = base64.urlsafe_b64decode(audio)

        # # saving the file
        audio_file = open(path, 'wb')
        audio_file.write(audio_data)

        # predicting student
        res = predict_speaker(path)
        print(res)

        # student = Student.objects.filter(roll_no=roll)
        # print(student)
        # attendence_obj = Attendance.objects.create(student_atnd=student[0], teacher=str(teacher), course=course)
        # attendence_obj.save()

        return JsonResponse({"response": "Attendence Marked", "res": str(res[0])})

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

