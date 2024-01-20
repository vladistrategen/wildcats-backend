from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist

def health_check(request):
    return JsonResponse({"status": "ok"})

def index(request):
    return render(request, 'index.html')
    
def login(request):
    try:
        return render(request, 'accounts/login.html')
    except TemplateDoesNotExist :
        return render(request, 'main_index_not_fount.html')
    
def signup(request):
    try:
        return render(request, 'accounts/signup.html')
    except TemplateDoesNotExist :
        return render(request, 'main_index_not_fount.html')
    
