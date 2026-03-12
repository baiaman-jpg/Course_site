from rest_framework import serializers
from .models import *


class TeacherNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkTeacher
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    networks = TeacherNetworkSerializer(source='networkteacher_set', many=True)

    class Meta:
        model = Teacher
        fields ='__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields ='__all__'


class ChapterSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Chapter
        fields = [
            'id',
            'chapter_name',
            'lessons'
        ]



class CourseListSerializer(serializers.ModelSerializer):


    class Meta:
        model = Course
        fields = [
            'id',
            'course_name',
            'course_description',
            'level',
            'language',
            'price',
            'created_by',
            'course_picture',
            'is_certificate',
        ]

class CourseDetailSerializer(serializers.ModelSerializer):

    created_by = TeacherSerializer()

    class Meta:
        model = Course
        fields = [
            'id',
            'course_name',
            'course_description',
            'language',
            'level',
            'price',
            'created_by',
            'is_certificate'
        ]





class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ['id','option_name']


class QuestionSerializer(serializers.ModelSerializer):

    options = OptionSerializer(source='option_set', many=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'question_name',
            'score',
            'options'
        ]


class ExamListSerializer(serializers.ModelSerializer):

    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = [
            'id',
            'exam_name',
            'duration',
            'questions_count'
        ]

    def get_questions_count(self,obj):
        return obj.question_set.count()


class ExamDetailSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(source='question_set', many=True)

    class Meta:
        model = Exam
        fields = [
            'id',
            'exam_name',
            'duration',
            'questions'
        ]

class CertificateSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    course_name = serializers.ReadOnlyField(source='course.course_name')
    student_name = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Certificate
        fields = [
            'id',
            'course',
            'course_name',
            'student',
            'student_name',

        ]