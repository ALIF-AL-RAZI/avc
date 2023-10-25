from django import forms
from .models import Course, Comment, Reply, Lecture, Enrollment, Attendance


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'duration', 'instructor', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('name', 'course', 'date', 'start_time', 'end_time')


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('user', 'course')


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('lecture', 'student', 'status')
        widgets = {
            'lecture': forms.HiddenInput(),
            'student': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        labels = {"body":"Comment:"}

        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':70, 'placeholder':"Enter Your Comment"}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_body',)

        widgets = {
            'reply_body': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'cols':10}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ReplyForm, self).__init__(*args, **kwargs)