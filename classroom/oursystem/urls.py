from django.urls import path
from oursystem import views

app_name='oursystem'
urlpatterns = [
    path("", views.CourseListView.as_view(), name='course_list'),
    path("course/create/", views.create_course, name='course_create'),
    path("course/<int:pk>/", views.CourseDetailView.as_view(), name='course_detail'),
    path("course/<int:pk>/update/", views.CourseUpdateView.as_view(), name='course_update'),
    path("course/<int:pk>/delete/", views.CourseDeleteView.as_view(), name='course_delete'),
    path("course/join_video_meeting/", views.join_video_meeting, name='join_video_meeting'),
]
