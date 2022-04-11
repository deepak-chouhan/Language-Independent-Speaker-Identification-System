from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def record(request):
    return render(request, "AudioProcessing/index.html")

@csrf_exempt
def save(request):
    if request.method == "POST":
        print("Hey")
        print(request.POST["audio"])
        return JsonResponse({"message": "req handled"})
