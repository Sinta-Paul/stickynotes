from django.contrib import admin
from .models import Project,Member,Todo,Schedule,Progress,Resource
# Register your models here.

admin.site.register(Member)
admin.site.register(Project)
admin.site.register(Todo)
admin.site.register(Schedule)
admin.site.register(Progress)
admin.site.register(Resource)