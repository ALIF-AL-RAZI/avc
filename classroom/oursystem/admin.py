from django.contrib import admin
from oursystem.models import Course, Comment, Reply
# Register your models here.Comment
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Reply)