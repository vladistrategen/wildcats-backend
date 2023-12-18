# views.py

from django.shortcuts import render
from .forms import SignUpForm

def signup_view(request):
    form = SignUpForm()  # Or pass request.POST or request.FILES if processing a submitted form
    return render(request, 'accounts/signup.html', {'form': form})  # The context variable here is named 'form'
