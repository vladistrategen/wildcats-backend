# views.py
from django.shortcuts import render, redirect
from .forms import PaymentForm, SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import csv
from django.contrib.auth.models import Group
from django.contrib import messages
    
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Log in the user
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('/login/')  # Redirect to the home page after successful registration
        else:
            messages.error(request, 'Error in registration. Please correct the form.')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page, e.g., home page
            return redirect('home')  # Replace 'home' with the name of your home URL
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def home_view(request):
    return render(request, 'accounts/home.html')


@login_required
def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Save user's information to a CSV file
            username = request.user.username
            card_number = form.cleaned_data['card_number']

            file_path = 'payment_data.csv'# Specify the absolute path
            with open(file_path, 'a', newline='') as csvfile:
                fieldnames = ['Username', 'CardNumber']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Check if the file is empty, and write the header if necessary
                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow({'Username': username, 'CardNumber': card_number})

            # Add user to PremiumUsers group
            premium_user_group = Group.objects.get(name='PremiumUser')
            request.user.groups.add(premium_user_group)

            # Remove the user from the free user group if they were in it
            free_user_group = Group.objects.get(name='FreeUser')  # Assuming you have a group named 'FreeUser'
            request.user.groups.remove(free_user_group)

            # Redirect the user after successful payment
            return redirect('home')
    else:
        form = PaymentForm()

    return render(request, 'accounts/payment.html', {'form': form})
