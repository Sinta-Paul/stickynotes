from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Progress,Project,Member,Todo,Schedule,User,Resource
from django.contrib.auth import authenticate,login,logout
from django.db.models.functions import Now  
import datetime

from datetime import timedelta

# Create your views here.
def home(request):
    return render(request,'base/home.html')

def logoutpage(request):
    logout(request)
    return redirect('home')

def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        projectname=request.POST.get('projectname')
        try:
            user=User.objects.get(username=username)
        except:
            print("login error")
        user=authenticate(username=username,password=password,projectname=projectname)
        if user is not None:
            login(request,user)
            return redirect('main',user,projectname)
        else:
            print("login failed")
    return render(request,'base/login.html')

def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        projectname=request.POST.get('projectname')
        pr_confirm=request.POST.get('addproject')
        user=User.objects.create_user(username,password=password)
        user.save()
        member=Member.objects.create(user=user,projectname=projectname)
        member.save()
        if (pr_confirm == 'True'):
            print(projectname)
            project=Project.objects.create(name=projectname)
            project.save()
            project.members.add(member)
            return redirect('schedule',user,projectname)
        login(request,user)
        return redirect('main',user,projectname)
    return render(request,'base/signup.html')

def main(request,user,projectname):
    project=Project.objects.get(name=projectname)

    if request.method=='POST':
        if 'progress' in request.POST:
            user=User.objects.get(username=user)
            commit=request.POST.get('commit')
            Progress.objects.create(user=user,project=project,commit=commit)
            return redirect('main',user,projectname)
        elif 'resource' in request.POST:
            link=request.POST.get('link')
            Resource.objects.create(project=project,link=link)
            return redirect('main',user,projectname)
        elif 'task' in request.POST:
            task=request.POST.get('tasks')
            Todo.objects.create(project=project,tasks=task)
            return redirect('main',user,projectname)
    
    members=Member.objects.filter(Q(projectname__icontains=project))
    schedule=Schedule.objects.filter(Q(project=project))
    progress=Progress.objects.filter(Q(project=project))
    tasks=Todo.objects.filter(Q(project=project))
    links=Resource.objects.filter(Q(project=project))

    start=datetime.date.today()
    end=start+datetime.timedelta(days=2)
    print(start)
    print(end)
    alerts=Schedule.objects.filter(Q(date__range=[start,end])&Q(project=project))
    print(alerts)
    context={'user':user,'members':members,'schedule':schedule,'progress':progress,'tasks':tasks,'projectname':projectname,'links':links,'alerts':alerts}
    return render(request,'base/main.html',context)

def markasdone(request,user,projectname,pk):
    task=Todo.objects.get(id=pk)
    task.delete()
    return redirect('main',user,projectname)

def create_schedule(request,user,projectname):
    user=User.objects.get(username=user)
    if request.method=='POST':
        title=request.POST.get('title')
        date=request.POST.get('date')
        Schedule.objects.create(project=Project.objects.get(name=projectname),title=title,date=date)
        if request.POST.get('addschedule')=='True':
            return redirect('schedule',user,projectname)
        else:
            login(request,user)
            return redirect('main',user,projectname)
    project=Project.objects.get(name=projectname)
    schedule=Schedule.objects.filter(project=project)
    context={'schedule':schedule}
    return render(request,'base/schedule.html',context)