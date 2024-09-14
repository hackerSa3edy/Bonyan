from django.contrib import admin
from user_profile.models import User, ActivationToken

# Register your models here.
admin.site.register(User)
admin.site.register(ActivationToken)
