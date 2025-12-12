from django.shortcuts import get_object_or_404, render

from .models import Course, Subject, Teacher


def home(request):
    courses = (
        Course.objects.select_related("subject", "owner")
        .prefetch_related("modules")
        .all()[:6]
    )
    teachers = Teacher.objects.filter(is_active=True)[:4]
    subjects = Subject.objects.all()
    return render(
        request,
        "edukate/index.html",
        {"courses": courses, "teachers": teachers, "subjects": subjects},
    )


def about(request):
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, "edukate/about.html", {"teachers": teachers})


def course_list(request):
    courses = Course.objects.select_related("subject", "owner").prefetch_related(
        "modules"
    )
    subjects = Subject.objects.all()
    subject_slug = request.GET.get("subject")
    if subject_slug:
        courses = courses.filter(subject__slug=subject_slug)
    return render(
        request,
        "edukate/course.html",
        {"courses": courses, "subjects": subjects, "active_subject": subject_slug},
    )


def course_detail(request, slug: str):
    course = get_object_or_404(
        Course.objects.select_related("owner", "subject").prefetch_related(
            "modules__contents"
        ),
        slug=slug,
    )
    related_courses = (
        Course.objects.exclude(pk=course.pk)
        .select_related("subject", "owner")
        .order_by("-created_at")[:3]
    )
    subjects = Subject.objects.all()
    recent_courses = Course.objects.select_related("subject", "owner").order_by(
        "-created_at"
    )[:4]
    return render(
        request,
        "edukate/detail.html",
        {
            "course": course,
            "related_courses": related_courses,
            "subjects": subjects,
            "recent_courses": recent_courses,
        },
    )


def contact(request):
    return render(request, "edukate/contact.html")


def features(request):
    return render(request, "edukate/feature.html")


def team(request):
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, "edukate/team.html", {"teachers": teachers})


def testimonials(request):
    return render(request, "edukate/testimonial.html")
