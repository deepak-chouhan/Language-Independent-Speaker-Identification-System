from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
import base64

def record(request):
    return render(request, "AudioProcessing/index.html")

@csrf_exempt
def save(request):
    if request.method == "POST":

        # array of base64 string
        audio = request.POST.getlist("audio[]")
        return JsonResponse({"resp": "handled"})

@csrf_exempt          
def Student_reg(request):
    if request.method=="POST":

        # array of base64 string
        audios = request.POST.getlist("audio[]")
        name=(request.POST.getlist("name")[0])
        batch=request.POST.getlist("batch")[0]
        rollno=request.POST.getlist("roll_no")[0]
        newstudent=Student.objects.create(name=name,batch=batch,roll_no=rollno)
        newstudent.save()
        i = 0
        for audio in audios:
            audio_data=base64.b64decode(audio)
            string1="newsrc/" + str(rollno)+"__" + str(name) + "__" + str(i)+'.mp3'
            i += 1
            print(string1)

            # saving the file
            with open(string1,'wb') as aud:
                aud.write(audio_data)
            audioobj = Audio.objects.create(student_roll=rollno, audiofile=string1)
            audioobj.save
    return render(request,"AudioProcessing/student.html")

