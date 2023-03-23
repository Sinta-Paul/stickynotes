from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    projectname=models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name=models.CharField(max_length=200)
    members=models.ManyToManyField(Member)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    project=models.ForeignKey(Project,on_delete=models.SET_NULL,null=True)
    title=models.CharField(max_length=200)
    date=models.DateField()

    def __str__(self):
        return self.title

class Todo(models.Model):
    project=models.ForeignKey(Project,on_delete=models.SET_NULL,null=True)
    tasks=models.CharField(max_length=200)
    updated=models.DateTimeField(auto_now=True)

class Progress(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    project=models.ForeignKey(Project,on_delete=models.SET_NULL,null=True)
    commit=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)

class Resource(models.Model):
    project=models.ForeignKey(Project,on_delete=models.SET_NULL,null=True)
    link=models.URLField(max_length=1000)

