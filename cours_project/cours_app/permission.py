from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Разрешение только для администраторов.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsTeacher(permissions.BasePermission):
    """
    Разрешение только для учителей.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsStudent(permissions.BasePermission):
    """
    Разрешение только для студентов.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешение изменять объект только его владельцу (например, созданному учителем или студентом) или администратору.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        # Для Teacher/Student моделей
        if hasattr(obj, 'student') and obj.student == request.user:
            return True
        if hasattr(obj, 'teacher') and obj.teacher == request.user:
            return True
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        return False