from django.http import JsonResponse
from django.shortcuts import render

def health_check(request):
    return JsonResponse({"status": "ok"})

def index(request):
    return render(request, 'index.html')