from django.utils import timezone
from django.contrib.auth.models import User
from models import Profile
import pytz
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated():
            user = User(username = request.user)
            profile = Profile( user = user )
            timezone.activate(pytz.timezone(profile.tz))
        else:
            timezone.deactivate()
