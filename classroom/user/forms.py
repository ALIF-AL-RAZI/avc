from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfileInfo

class UserForm(UserCreationForm):
    email=forms.EmailField()
    
    class Meta():
        model=User
        fields=('username', 'first_name', 'last_name', 'password1', 'password2')

        lebels={
            'password1':'Password',
            'password2': 'Confirm Password'
        }


class UserProfileInfoForm(forms.ModelForm):

    teacher = 'teacher'
    student = 'student'

    user_types = [
        (teacher, 'teacher'),
        (student, 'student')
    ]
    user_type = forms.ChoiceField(required=True, choices=user_types)

    class Meta():
        model=UserProfileInfo
        fields=('profile_photo', 'user_type')