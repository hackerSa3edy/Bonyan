from django.contrib import admin
from user_profile.models import User, ActivationToken, Student, Instructor

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(ActivationToken)
