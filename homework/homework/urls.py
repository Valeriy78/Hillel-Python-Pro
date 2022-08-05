"""homework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
import string
from random import choice
from django.http import HttpRequest, HttpResponse


def home_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello, Serhii!')


def article_view(request: HttpRequest, article_id: int, article_slug: str) -> HttpResponse:
    response = f"""
    {article_id}
    {article_slug}
    """
    return HttpResponse(response)


def password_view(request: HttpRequest, password: str) -> HttpResponse:
    if not len(password) == 8:
        return HttpResponse('Invalid password')
    for char in password:
        if not (char.isalpha() or char.isdigit()):
            return HttpResponse('Invalid password')
    return HttpResponse('Password is valid')


def generate_password(request: HttpRequest, length: int) -> HttpResponse:
    password = ''
    characters = string.ascii_letters + string.digits
    for i in range(length):
        password += choice(characters)
    return HttpResponse(password)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', home_view),
    path('home/', home_view),
    path('', home_view),
    path('article/<int:article_id>/<slug:article_slug>', article_view),
    path('password/<str:password>', password_view),
    path('password/generate/<int:length>', generate_password),
]
