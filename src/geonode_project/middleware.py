# -*- coding: utf-8 -*-
"""Force public HTTPS origin when TLS is terminated at luc-nginx (:8443)."""

from urllib.parse import urlparse

from django.conf import settings


class ForceHttpsSchemeMiddleware:
    """GeoNode nginx talks to Django over http and often forwards Host /
    X-Forwarded-Proto without the public :8443 port. DRF then emits
    https://host/... (no port) or http://... links; MapStore follows them
    and either hits LUC :443 or gets mixed-content blocked.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        parsed = urlparse(settings.SITEURL)
        host = parsed.hostname or ""
        if parsed.port:
            host = f"{host}:{parsed.port}"
        self._public_host = host

    def __call__(self, request):
        request.META["HTTP_X_FORWARDED_PROTO"] = "https"
        request.META["wsgi.url_scheme"] = "https"
        if self._public_host:
            request.META["HTTP_HOST"] = self._public_host
            request.META["HTTP_X_FORWARDED_HOST"] = self._public_host
        return self.get_response(request)
