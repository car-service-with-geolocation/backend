from django.contrib.gis.geoip2 import GeoIP2
from car_service.settings import DEBUG


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_geoip_from_request(request):
    g = GeoIP2()
    ip = get_client_ip(request)
    try:
        if DEBUG:
            # Тестовый ip для Москвы
            return g.city('83.220.236.105')
        return g.city(ip)
    except Exception:
        return None
