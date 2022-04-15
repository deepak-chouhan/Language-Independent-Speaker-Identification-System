from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *

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
    # form=Studentform()
    if request.method=="POST":

        # array of base64 string
        audios = request.POST.getlist("audio[]")
        print(request.POST)

        # print("123hey 34")
        # if form.is_valid():
        #     print("123hey 34")
        #     form=Studentform(request.POST)
        #     print("hey")
        #     rollno= form.cleaned_data.get("roll_no")
        #     form.save()
        #     val=len(base64file)
        #     audio = Audio.objects.create(student_roll=rollno,val=val)
        #     audio.save()
        # return JsonResponse({"resp": "handled"})
    return render(request,"AudioProcessing/student.html")

