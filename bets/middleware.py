from django.utils import timezone
from django.contrib.auth.models import User
from models import Profile
import pytz
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated():
            timezone.activate(pytz.timezone(request.user.profile.tz))
        else:
            timezone.deactivate()
