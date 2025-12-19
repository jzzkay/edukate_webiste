from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Subject, Teacher
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from .forms import RegisterForm

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

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            message = render_to_string('email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            mail_subject = 'Activate your Edukate account'
            email = EmailMessage(mail_subject, message, to=[form.cleaned_data.get('email')])
            email.send()
            return render(request, 'check_email.html')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')