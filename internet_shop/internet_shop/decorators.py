"""
Internet_shop project decorators
"""

from functools import wraps

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


REDIRECT_URL = reverse_lazy("homepage")


def is_staff(view_func, redirect_url=REDIRECT_URL):
    """Verify that the current user is staff"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(redirect_url)
    return wrapper


def is_not_staff(view_func, redirect_url=REDIRECT_URL):
    """Verify that the current user is not staff"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(redirect_url)
    return wrapper
