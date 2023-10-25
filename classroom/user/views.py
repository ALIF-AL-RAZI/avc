from oursystem.models import Course
from django.views.generic.base import TemplateView
from .forms import UserForm, UserProfileInfoForm
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfileInfo
from django.views.generic import CreateView
from django.views.generic import TemplateView

# Create your views here.


class starting_page(TemplateView):
    template_name= "user/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.all()
        teachers = UserProfileInfo.objects.filter(user_type='teacher')
        context['courses'] = courses
        context['teachers'] = teachers
        return context


def register(request):
    resistered=False
    
    if request.method == "POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            
            resistered=True
        else:
            print(user_form.errors, profile_form.errors)

    else: 
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request, 'user/registration.html', {
        'resistered': resistered,
        'user_form': user_form,
        'profile_form': profile_form }
    )
            
def user_login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account is not active")
        else:
            return HttpResponse("Please use correct id and password")
    else:
        return render(request, 'user/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
