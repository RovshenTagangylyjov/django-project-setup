from django.core.cache import cache
from django.db import connection
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Basic health check endpoint for load balancers."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)


class ReadinessCheckView(APIView):
    """Readiness check verifying database and cache connections."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        checks = {
            "database": self._check_database(),
            "cache": self._check_cache(),
        }

        all_healthy = all(check["status"] == "healthy" for check in checks.values())
        http_status = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(
            {"status": "ready" if all_healthy else "not_ready", "checks": checks},
            status=http_status,
        )

    def _check_database(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def _check_cache(self):
        try:
            cache.set("health_check", "ok", timeout=10)
            value = cache.get("health_check")
            if value == "ok":
                return {"status": "healthy"}
            return {"status": "unhealthy", "error": "Cache read/write failed"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
