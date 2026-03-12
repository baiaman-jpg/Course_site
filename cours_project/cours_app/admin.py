from django.contrib import admin
from .models import *

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class OptionInline(admin.TabularInline):
    model = Option
    extra = 2


class NetworkTeacherInline(admin.TabularInline):
    model = NetworkTeacher
    extra = 1


class ChapterAdmin(admin.ModelAdmin):
    inlines = [LessonInline]


class ExamAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


class TeacherAdmin(admin.ModelAdmin):
    inlines = [NetworkTeacherInline]


admin.site.register(Course)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Language)

admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Lesson)

admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student)

admin.site.register(Review)
admin.site.register(Certificate)