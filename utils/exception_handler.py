import logging

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


def exception_handler(exc, context):
    """Custom exception handler with consistent error format."""

    # Call DRF's default exception handler first
    response = drf_exception_handler(exc, context)

    # Handle Django's ValidationError
    if isinstance(exc, ValidationError):
        if hasattr(exc, "message_dict"):
            data = {"detail": exc.message_dict}
        else:
            data = {"detail": exc.messages}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # Handle Django's Http404
    if isinstance(exc, Http404):
        return Response(
            {"detail": "Not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Handle Django's PermissionDenied
    if isinstance(exc, PermissionDenied):
        return Response(
            {"detail": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # If response is None, it's an unhandled exception
    if response is None:
        logger.exception("Unhandled exception: %s", exc)
        return Response(
            {"detail": "Internal server error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Normalize error response format
    if isinstance(response.data, dict):
        if "detail" not in response.data:
            response.data = {"detail": response.data}
    elif isinstance(response.data, list):
        response.data = {"detail": response.data}

    # Add error code if available
    if isinstance(exc, APIException) and exc.default_code:
        response.data["code"] = exc.default_code

    return response
