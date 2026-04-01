import logging
import time
import uuid

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    """Middleware to add a unique request ID to each request for tracing."""

    HEADER_NAME = "X-Request-ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get or generate request ID
        request_id = request.headers.get(self.HEADER_NAME) or str(uuid.uuid4())
        request.request_id = request_id

        response = self.get_response(request)

        # Add request ID to response headers
        response[self.HEADER_NAME] = request_id
        return response


class RequestLoggingMiddleware:
    """Middleware to log request/response details."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        request_id = getattr(request, "request_id", "-")

        logger.info(
            "request_id=%s method=%s path=%s status=%s duration=%.3fs",
            request_id,
            request.method,
            request.path,
            response.status_code,
            duration,
        )

        return response
