from django.contrib.gis.geoip2 import GeoIP2


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
    if ip in '127.0.0.1' or ip in 'localhost':
        return None
    return g.city(ip)
