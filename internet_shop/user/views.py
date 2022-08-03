from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


user = {
    "id": 1,
    "username": "shorodilov",
    "first_name": "Serhii",
    "last_name": "Horodilov"
}


def user_profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'user.html', user)

