from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group

def create_user(request):
    # Your user creation logic here

    user = User.objects.create(username='example_user', password='example_password')

    # Assign the user to a group based on their role
    #user.groups.add(free_user_group)  # Replace with the appropriate group for the user

    # Rest of your user creation logic
