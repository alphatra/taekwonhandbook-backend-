from typing import Any
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    response = exception_handler(exc, context)
    request = context.get("request")
    request_id = None
    if request is not None:
        request_id = request.headers.get("X-Request-ID") or request.META.get("HTTP_X_REQUEST_ID")
    if response is not None:
        data = {
            "code": getattr(exc, "default_code", exc.__class__.__name__),
            "detail": response.data if isinstance(response.data, (dict, list)) else str(response.data),
            "request_id": request_id,
        }
        response.data = data
    return response

