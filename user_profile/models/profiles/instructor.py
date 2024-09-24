from django.db import models
from user_profile.models.profiles.user import User

class Instructor(User):
    specialized_in = models.CharField(max_length=100)