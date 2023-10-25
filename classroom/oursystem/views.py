from django.views.generic.base import View
from oursystem.models import Course, Comment
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (TemplateView, CreateView,
                                    UpdateView, DeleteView, DetailView, ListView, FormView)
from django.urls import reverse_lazy, reverse
from .forms import CourseForm, CommentForm, ReplyForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

class CourseListView(ListView):
    context_object_name = 'courses'
    model = Course
    template_name = 'oursystem/course_list_view.html'

# def course_view(request):
#     context = {}
#
#     # add the dictionary during initialization
#     context["dataset"] = Course.objects.all()
#
#     return render(request, "oursystem/course_list_view.html", context)

"""class JoinClass(DetailView, FormView):
    form_class = CourseForm
    fields = ('code')
    context_object_name = 'subjects'
    model = Subject
    template_name = 'oursystem/join_class.html'


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('oursystem:course_list',kwargs={'slug':self.object.slug})"""

# def course_detail(request, course_id):
#     models = Course
#     form_class = CommentForm
#     second_form_class = ReplyForm
#     course = get_context_data(models, pk=course_id)
#     context = {'course': course}
#     return render(request, 'course_detail.html', context)


class CourseDetailView(DetailView):
    context_object_name = 'course'
    model = Course
    template_name = 'oursystem/course_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm
    queryset = Course.objects.all()  # Define the queryset for the view

    def get_context_data(self, **kwargs):
        # import pdb
        # pdb.set_trace()
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        import pdb
        pdb.set_trace()
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        if form_name == 'form':
            form = self.form_class(request=self.request, data=request.POST)
            if form.is_valid():
                return self.form_valid(form)
        elif form_name == 'form2':
            form = self.second_form_class(request=self.request, data=request.POST)
            if form.is_valid():
                return self.form2_valid(form)

        # If the form is invalid or not submitted, re-render the page with the form
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('oursystem:course_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.course_name = self.object.name
        fm.course_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


def create_course(request):
    if request.method == 'POST':
        import pdb
        pdb.set_trace()
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.updated_by = request.user
            course.save()
            return redirect('oursystem:course_list')
    else:
        form = CourseForm()

    return render(request, 'oursystem/course_create.html', {'form': form})


class CourseCreateView(CreateView):
    # #fields = ('course_id','name','section','code')

    model = Course
    template_name = 'oursystem/course_create.html'
    form_class = CourseForm
    # context_object_name = 'course'



    # fields = ['name', 'code', 'description', 'duration', 'instructor', 'start_date', 'end_date']

    def get_success_url(self):
        return reverse_lazy('oursystem:course_list')

    def form_valid(self, form):
        import pdb
        pdb.set_trace()
        # def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.updated_by = self.request.user
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
        # form.instance.created_by = self.request.user
        # form.instance.updated_by = self.request.user
        # return super().form_valid(form)

class CourseUpdateView(UpdateView):
    fields = ('name', 'description', 'duration', 'start_date', 'end_date')
    model = Course
    template_name = 'oursystem/course_update.html'
    context_object_name = 'courses'


class CourseDeleteView(DeleteView):
    model = Course
    context_object_name = 'courses'
    template_name = 'oursystem/course_delete.html'

    def get_success_url(self):
        self.object = self.get_object()
        print(self.object)
        subject = self.object.subject
        return reverse_lazy('oursystem:course_list', kwargs={'pk': self.pk})

@login_required
def join_video_meeting(request, **kwargs):
    user_name = request.user.username  # Get the username
    context = {'user_name': user_name}  # Create a context dictionary
    return render(request, "oursystem/room.html", context)