from django.contrib import admin

from .models import Content, Course, Enrollment, File, Image, Module, Subject, Teacher, Text, Video

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "expertise", "experience_years", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "expertise")

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "owner", "created_at")
    list_filter = ("subject", "created_at")
    search_fields = ("title", "overview")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    search_fields = ("title", "overview")

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("module", "content_type", "object_id")
    list_filter = ("content_type",)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "enrolled_at")
    list_filter = ("enrolled_at",)
    search_fields = ("user__username", "course__title")
    date_hierarchy = "enrolled_at"

admin.site.register(Text)
admin.site.register(File)
admin.site.register(Video)
admin.site.register(Image)
