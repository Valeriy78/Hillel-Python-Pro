"""
User application views
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, LoginForm, ProfileEditForm
from purchase.models import Cart


@login_required(login_url=reverse_lazy("login"))
def user_profile(request: HttpRequest) -> HttpResponse:
    """User profile view implementation"""

    return render(request, "user.html")


@require_http_methods(["GET", "POST"])
def register_view(request: HttpRequest) -> HttpResponse:
    """Register user view"""

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.create_user()
            if not new_user.is_staff:
                cart = Cart(customer=new_user)
                cart.save()
            return HttpResponseRedirect(reverse_lazy("login"))
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    """Login user view"""

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return HttpResponseRedirect(reverse_lazy("homepage"))
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@login_required(login_url=reverse_lazy("login"))
def logout_view(request: HttpRequest) -> HttpResponse:
    """Logout user view"""

    logout(request)
    return HttpResponseRedirect(reverse_lazy("homepage"))


@login_required(login_url=reverse_lazy("login"))
def deactivate_view(request: HttpRequest) -> HttpResponse:
    """Deactivate user view"""

    request.user.is_active = False
    request.user.save()
    logout(request)
    return HttpResponseRedirect(reverse_lazy("homepage"))


@require_http_methods(["GET", "POST"])
@login_required(login_url=reverse_lazy("login"))
def profile_edit_view(request: HttpRequest) -> HttpResponse:
    """Edit user profile"""

    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            user.first_name = form.get_items()["first_name"]
            user.last_name = form.get_items()["last_name"]
            user.email = form.get_items()["email"]
            user.save()
            return HttpResponseRedirect(reverse_lazy("user"))
    else:
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        form = ProfileEditForm({"first_name": first_name, "last_name": last_name, "email": email})
    return render(request, "profile_edit.html", {"form": form})
