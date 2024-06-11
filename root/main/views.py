from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist!')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password does not exist!')

    context = {'page': page}
    return render(request,'main/login_register.html',context)


def logout_user(request):
    logout(request)
    return redirect('home')

def registerpage(request):
    # page = 'register'
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

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # 'q' only if it contains something else empty
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)) # icontains is case insensitive
    topics = Topic.objects.all()
    room_count = rooms.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'main/home.html',context)


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

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'main/room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = room_form()
    if request.method == 'POST':
        form = room_form(request.POST) # passes the form from django
        if form.is_valid:
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request,'main/create_room.html',context)


@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = room_form(instance=room) # passes the room values to django ModelForm for prefilling

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
       form = room_form(request.POST, instance=room) # passes the form from django
       if form.is_valid:
            form.save()
            return redirect('home')  
       
    context = {'form':form}
    return render(request,'main/create_room.html',context)


@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'main/delete.html',{'obj':room})


@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'main/delete.html',{'obj':message})


@login_required(login_url='login')
def edit_message(request,pk):
    message = Room.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
       form = room_form(request.POST, instance=room) # passes the form from django
       if form.is_valid:
            form.save()
            return redirect('home')  
       
    context = {'message':message}
    return render(request,'main/create_room.html',context)