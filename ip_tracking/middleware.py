import logging
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
import ipinfo
from django.core.cache import cache

logger = logging.getLogger(__name__)
ACCESS_TOKEN = '36fd9b934636e8'
handler = ipinfo.getHandler(ACCESS_TOKEN)

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', '')
        
        # Task 1: IP Blacklist
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked")

        path = request.path

        # Task 2: IP Geolocation
        geo = cache.get(ip)
        if not geo:
            try:
                details = handler.getDetails(ip)
                geo = {'country': details.country_name, 'city': details.city}
            except:
                geo = {'country': '', 'city': ''}
            cache.set(ip, geo, 86400)  # Cache for 24 hours

        # Log request
        RequestLog.objects.create(ip_address=ip, path=path, country=geo['country'], city=geo['city'])

        return self.get_response(request)
