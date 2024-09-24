from django.db import models
from levels.models.levels import Level
from user_profile.models.profiles.user import User
from levels.models.department import Department

class Student(User):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='students')
    courses = models.ManyToManyField('levels.Course', through='levels.CourseStudentEnrollment')
