from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("courses/", views.course_list, name="course_list"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("contact/", views.contact, name="contact"),
    path("features/", views.features, name="features"),
    path("team/", views.team, name="team"),
    path("testimonials/", views.testimonials, name="testimonials"),
]

