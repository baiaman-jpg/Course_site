from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, ExamViewSet, CertificateViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('lessons', LessonViewSet)
router.register('exams', ExamViewSet)
router.register('certificates', CertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]