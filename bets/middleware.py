from django.utils import timezone
from django.contrib.auth.models import User
from bets.models import Profile
import pytz
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            # is_authenticated is a property on Django 4+
            try:
                timezone.activate(pytz.timezone(user.profile.tz))
            except Exception:
                timezone.deactivate()
        else:
            timezone.deactivate()
