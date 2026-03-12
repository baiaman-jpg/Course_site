from modeltranslation.translator import TranslationOptions, register
from .models import Course, Category, SubCategory, Chapter, Lesson


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('subcategory_name',)


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = (
        'course_name',
        'course_description',
    )


@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = (
        'chapter_name',
        'chapter_description',
    )


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = (
        'lesson_name',
        'content',
    )