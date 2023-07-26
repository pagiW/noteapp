from django.shortcuts import render, redirect
from .models import *
from dotenv import load_dotenv
from jwt import encode, decode
import datetime
import os

load_dotenv()


# Create your views here.
def index(request):
    return render(request, 'index.html')
def home(request, id):
    pk = decode(id, os.getenv('SECRET'), algorithms=[os.getenv('ALGORITHM')])
    user = UserModel.objects.get(pk=int(pk['id']))
    notes = Notes.objects.filter(user=user)
    return render(request, 'notes.html', context={'name': user.name, 'notes': notes, 'id': id})

def newnote(request, id):
    pk = decode(id, os.getenv('SECRET'), algorithms=[os.getenv('ALGORITHM')])
    user = UserModel.objects.get(pk=int(pk['id']))
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Notes.objects.create(title=title, content=content, user=user, time=datetime.datetime.now())
        return redirect(f'/home/{id}')
    return render(request, 'newnote.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = encode({'pass': request.POST['password']}, os.getenv('SECRET'), algorithm=os.getenv('ALGORITHM'))
        email = request.POST['email']
        user = UserModel.objects.create(name=name, password=password, email=email)
        return redirect(f'home/{encode({"id": user.pk, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}, os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM"))}')
    return render(request, 'signup.html')

def login(request):
    verify = False
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            password = encode({'pass': request.POST['password']}, os.getenv('SECRET'), algorithm=os.getenv('ALGORITHM'))
            user = UserModel.objects.get(name=name, password=password, email=email)
            return redirect(f'home/{encode({"id": user.pk, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}, os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM"))}')
        except:
            verify = True
    return render(request, 'login.html', {'verify': verify})

def delete(request, id, note):
    note = Notes.objects.get(pk=note)
    pk = decode(id, os.getenv('SECRET'), algorithms=[os.getenv('ALGORITHM')])
    user = UserModel.objects.get(pk=int(pk['id']))
    notes = Notes.objects.filter(user=user)
    return render(request, 'notes.html', context={'name': user.name, 'notes': notes, 'id': id, 'note': note})

def conf(request, id, note):
    note = Notes.objects.get(pk=note)
    pk = decode(id, os.getenv('SECRET'), algorithms=[os.getenv('ALGORITHM')])
    user = UserModel.objects.get(pk=int(pk['id']))
    if note.user == user:
        note.delete()
    
    return redirect(f'/home/{id}')

def mod(request, id, note):
    note = Notes.objects.get(pk=note)
    pk = decode(id, os.getenv('SECRET'), algorithms=[os.getenv('ALGORITHM')])
    user = UserModel.objects.get(pk=int(pk['id']))
    prop = False
    if user == note.user:
        prop = True

    if request.method == 'POST':
        note.title = request.POST['title']
        note.content= request.POST['content']
        note.time = datetime.datetime.now()
        note.save()
        return redirect(f'/home/{id}')
    return render(request, 'modnote.html', {'prop': prop, 'note': note})