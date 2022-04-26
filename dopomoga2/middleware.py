from django.http import HttpRequest
from django.utils import translation


def translate_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if not request.path.startswith("/admin"):
            translation.activate("uk")
        else:
            translation.deactivate_all()

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
