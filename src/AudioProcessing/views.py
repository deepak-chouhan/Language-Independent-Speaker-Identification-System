from django.shortcuts import render


def record(request):
    return render(request, "AudioProcessing/index.html")
