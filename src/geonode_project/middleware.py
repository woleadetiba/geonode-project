# -*- coding: utf-8 -*-
"""Force HTTPS scheme when TLS is terminated upstream (luc-nginx)."""


class ForceHttpsSchemeMiddleware:
    """GeoNode nginx proxies to Django over http and often sets
    X-Forwarded-Proto from $scheme (http). DRF then returns http:// API
    links; MapStore follows them and the browser blocks mixed content.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META["HTTP_X_FORWARDED_PROTO"] = "https"
        request.META["wsgi.url_scheme"] = "https"
        return self.get_response(request)
