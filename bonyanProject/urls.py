"""
URL configuration for bonyanProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # URL pattern for API views
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls.api_urls')),
    path('api/', include('question_management.urls')),
    path('api/', include('quiz_management.urls')),
    path('api/', include('quiz_participation.urls')),
    path('api/', include('user_profile.urls.api_urls')),

    # URL pattern for the web views
    path('', include('authentication.urls.web_urls')),
    path('', include('user_profile.urls.web_urls')),
]


def handle():
    for pattern in urlpatterns[1:]:
        print_pattern(pattern)

def print_pattern(pattern, prefix=''):
    if hasattr(pattern, 'url_patterns'):
        for sub_pattern in pattern.url_patterns:
            print_pattern(sub_pattern, prefix + pattern.pattern.regex.pattern)
    else:
        print(f'{prefix}{pattern.pattern.regex.pattern}')

# handle()