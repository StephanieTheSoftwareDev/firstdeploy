from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.utils import timezone
import pytz
from datetime import datetime
from models import *


def index(request):
    
    return render(request, 'testapp/index.html')

def reg(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
                print tag, error
                return redirect('/')
        elif len(errors) == 0:
            password=request.POST['pw']
            hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print "This is the hashed pw: ", hash1
            timezone.now()
            originaldate = datetime.strptime(request.POST['birthdate'], '%m/%d/%y')
            bdate = datetime.datetime(originaldate, tzinfo=pytz.UTC)
            # newdate = datetime.datetime.strptime(olddate,'%d.%m.%y').strftime('%Y-%m-%d')
            b = User(name=request.POST['name'], email=request.POST['email'], password=hash1, birthdate=bdate)
            b.save()
            request.session['user_id'] = b.id
            print request.session['user_id']
            return redirect('/appointments')


def appointments(request):
    nownownow = datetime.datetime.now()
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {'user': User.objects.get(id=request.session['user_id']),}
        bob = {'task': Task.objects.all()}
        return render(request, 'testapp/appointments.html', context, {'tasks': Task.objects.all()})

def login(request):
    if request.method == 'POST':
        errors1 = User.objects.log_validator(request.POST)
        
        if len(errors1):
            for tag, error in errors1.iteritems():
                messages.error(request, error, extra_tags=tag)
                print tag, error
            return redirect('/')
        elif len(errors1) == 0:
            c = self.get(email=request.POST['email'])
            request.session['user_id'] = c.id
            print request.session['user_id']
            return redirect('/appointments')

def logout(request):
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')
    else:
        request.session.clear()
        return redirect('/')


def addtask(request):
    print "first step after clicking on addtask"
    if request.method == 'POST':
        errors3 = User.objects.add_validator(request.POST)
        print "hello"
        # newdate = time.strptime(request.POST['task_date']," %m %d %Y")
        # print newdate
        # # olddate = request.POST['task_date']
        # # newdate = datetime.datetime.strptime(olddate,'%d.%m.%y').strftime('%Y-%m-%d')
        # person_type = Person_Type.objects.get(pers_type='Appellant') Person.objects.create(name='Adam', pers_type=person_type)
        this_user = User.objects.get(id=request.session['user_id'])
        # request.session['user_id'] = this_user.id
        Task.objects.create(task_name=request.POST['taskname'], task_time=request.POST['tasktime'], task_date=request.POST['taskdate'], users_id=this_user)
        # Task.objects.create(task_name=request.POST['taskname'], task_time=request.POST['tasktime'], task_date=request.POST['taskdate'], users=User.objects.get(request.session['user_id']))
       
        return redirect('/appointments')    
    else:
        print "hello else"
        return redirect('/appointments')