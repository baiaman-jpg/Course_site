from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


RoleChoices = (
    ('admin', 'admin'),
    ('teacher', 'teacher'),
    ('student', 'student'),
)


class UserProfile(AbstractUser):
    profile_picture = models.ImageField(upload_to='user_pictures', blank=True, null=True)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(70)],
        blank=True,
        null=True
    )


class Teacher(UserProfile):
    role = models.CharField(max_length=20, choices=RoleChoices)
    bio = models.TextField(blank=True, null=True)


class Student(UserProfile):
    role = models.CharField(max_length=20, choices=RoleChoices)


class NetworkStudent(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='networks'
    )
    network_name = models.CharField(max_length=32)
    network_url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.student.username} - {self.network_name}"


class NetworkTeacher(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='networks'
    )

    network_name = models.CharField(max_length=32)
    network_url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.teacher.username} - {self.network_name}"


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=32, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    def __str__(self):
        return self.subcategory_name


class Language(models.Model):
    language_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.language_name


class Course(models.Model):
    LevelChoices = (
        ('Easy', 'Easy'),
        ('Middle', 'Middle'),
        ('Pro', 'Pro'),
    )

    course_name = models.CharField(max_length=32)
    course_description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    level = models.CharField(max_length=32, choices=LevelChoices, default='Easy')

    price = models.DecimalField(decimal_places=2, max_digits=8)

    created_by = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    created_on = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    course_picture = models.ImageField(upload_to='course_pictures/')
    is_certificate = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.course_name} ({self.price})'


class Chapter(models.Model):
    chapter_name = models.CharField(max_length=32)
    chapter_description = models.TextField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='chapters'
    )

    def __str__(self):
        return f"{self.chapter_name} ({self.course.course_name})"


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=320)
    lesson_image = models.ImageField(upload_to='lesson_images/')
    lesson_file = models.FileField(upload_to='lesson_files/', null=True, blank=True)
    lesson_video = models.FileField(upload_to='lesson_videos/', null=True, blank=True)

    content = models.TextField()

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    def __str__(self):
        return f'{self.lesson_name} ({self.chapter.chapter_name})'


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=32)
    assignment_description = models.TextField()

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    due_date = models.DateField(verbose_name='Due date')

    def __str__(self):
        return f'{self.assignment_name} ({self.lesson.lesson_name})'


class Exam(models.Model):
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='exams'
    )

    exam_name = models.CharField(max_length=32)
    duration = models.DurationField()

    def __str__(self):
        return f'{self.exam_name} ({self.chapter.chapter_name})'


class Question(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_name = models.CharField(max_length=150)

    score = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )

    def __str__(self):
        return self.question_name


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options'
    )

    option_name = models.CharField(max_length=32)
    option_type = models.BooleanField()

    def __str__(self):
        return self.option_name


class Certificate(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='certificates'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='certificates'
    )

    certificate_url = models.FileField(upload_to='certificate_url/')
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Certificate for {self.student.username} ({self.course.course_name})'


class Review(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        null=True,
        blank=True
    )

    text = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.student.username} for {self.course.course_name}'


class ReviewLike(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    like = models.BooleanField()

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like for review {self.review.id}"