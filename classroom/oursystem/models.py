from django.db import models

# Create your models here.
from django.db import models
from django.template.defaultfilters import slugify
import os
from django.contrib.auth.models import User
from django.urls import reverse


def save_course_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.course_id:
        filename = 'course_files/{}/{}.{}'.format(instance.course_id,instance.course_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.course_id) + str('1')
            filename =  'course_images/{}/{}.{}'.format(instance.course_id,new_name, ext)
    return os.path.join(upload_to, filename)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    description = models.TextField(max_length=255, default='')
    duration = models.IntegerField(default=0)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    start_date = models.DateField(default='')
    end_date = models.DateField(default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created', default=None)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_updated', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('oursystem:course_list', kwargs={'pk': self.pk})


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date = models.DateField(default=None)
    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lecture_detail', args=[str(self.id)])

    class Meta:
        ordering = ['date', 'start_time']


class Comment(models.Model):
    course_name = models.ForeignKey(Course, null=True, on_delete=models.CASCADE,related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=20, choices=(
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'lecture')

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)


