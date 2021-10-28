from django.shortcuts import render,redirect
from  main.models import Room,Message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def index(request):
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            room_name = request.POST.get('room_name')
            room = Room.objects.get(room_name=room_name)
            if room:
                return redirect(f'/room/{room_name}/?name={name}')



    except Exception as e:
        print(e)


    return render(request, 'home/index.html')


def room(request, room_name):
    try:
        room = Room.objects.get(room_name=room_name)
        if room.room_name== room_name:
            reply = room.messages.all()


            return render(request, 'home/chatroom.html', {'room_name': room_name,'reply': reply})   
    except Exception as e:
        print(e)
    messages.warning(request, "No room exists" ) 
    return redirect("/")   



@login_required(login_url = '/account/login/')
def dashboard(request):
    try:
        if request.method == 'POST':
            user_obj = request.user.profile
       

            room_name = request.POST.get('room_name')
            if Room.objects.filter(room_name = room_name).first():
                messages.warning(request, "room already exists")

                return redirect('/dashboard/')
            room = Room(room_name=room_name,admin=user_obj)
            room.save()
            return redirect('/dashboard/')
        user_obj = request.user.profile
        print(user_obj)
        rooms = Room.objects.filter(admin=user_obj)
        print(rooms)
        return render(request, 'home/dashboard.html', {'rooms': rooms})

    except Exception as e:
        print(e)



    return render(request, 'home/dashboard.html')
