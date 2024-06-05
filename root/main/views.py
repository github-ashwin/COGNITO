from django.shortcuts import render,redirect
from django.db.models import Q
from .models import *
from .forms import *
# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # 'q' only if it contains something else empty
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)) # icontains is case insensitive
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'main/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request,'main/room.html',context)


def create_room(request):
    form = room_form()
    if request.method == 'POST':
        form = room_form(request.POST) # passes the form from django
        if form.is_valid:
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request,'main/create_room.html',context)


def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = room_form(instance=room) # passes the room values to django ModelForm for prefilling
    if request.method == 'POST':
       form = room_form(request.POST, instance=room) # passes the form from django
       if form.is_valid:
            form.save()
            return redirect('home')  
       
    context = {'form':form}
    return render(request,'main/create_room.html',context)


def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'main/delete.html',{'obj':room})