from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Course, Lesson, Exam, Certificate
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    LessonSerializer,
    ExamListSerializer,
    ExamDetailSerializer,
    CertificateSerializer
)

# -------------------------------
# Courses
# -------------------------------
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [AllowAny]  # все могут смотреть, админ может CRUD

    def get_serializer_class(self):
        if self.action in ['list']:
            return CourseListSerializer
        return CourseDetailSerializer

# -------------------------------
# Lessons
# -------------------------------
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

# -------------------------------
# Exams
# -------------------------------
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExamDetailSerializer
        return ExamListSerializer

# -------------------------------
# Certificates
# -------------------------------
class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]