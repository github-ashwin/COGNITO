from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# View for logging in a user
def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect!')

    context = {'page': page}
    return render(request, 'main/login_register.html', context)

# View for logging out a user
def logout_user(request):
    logout(request)
    return redirect('home')

# View for registering a new user
def registerpage(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)

    context = {'form': form}
    return render(request, 'main/login_register.html', context)

# View for displaying the home page with rooms and topics
def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'main/home.html', context)

# View for displaying a specific room and its messages
@login_required(login_url='login')
def room(request, pk):
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message_body = request.POST.get('body')

        if message_id:
            message = get_object_or_404(Message, id=message_id)
            if request.user == message.user:
                message.body = message_body
                message.save()
        else:
            Message.objects.create(
                user=request.user,
                room=room,
                body=message_body
            )
            room.participants.add(request.user)

        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'main/room.html', context)

# View for user profile
def user_profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() # host(user) is a foreign key in Room model
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request,'main/profile.html',context)

# View for creating a new room
@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'main/create_room.html', context)

# View for updating an existing room
@login_required(login_url='login')
def update_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')  
       
    context = {'form': form}
    return render(request, 'main/create_room.html', context)

# View for deleting a room
@login_required(login_url='login')
def delete_room(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj': room})

# View for deleting a message
@login_required(login_url='login')
def delete_message(request, pk):
    message = get_object_or_404(Message, id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj': message})

# View for editing a message
@login_required(login_url='login')
def edit_message(request, pk):
    message = get_object_or_404(Message, id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.body = request.POST.get('body')
        message.save()
        return redirect('home')
    
    context = {'message': message}
    return render(request, 'main/edit_message.html', context)
