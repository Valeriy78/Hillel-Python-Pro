"""
Internet_shop project mixins
"""

from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy


REDIRECT_URL = reverse_lazy("login")


class IsStaffMixin(AccessMixin):
    """Verify that the current user is staff"""

    login_url = REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
