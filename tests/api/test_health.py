import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestHealthEndpoints:
    def test_health_check_returns_200(self, api_client):
        url = reverse("health_check")
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["status"] == "healthy"

    def test_readiness_check_returns_200(self, api_client):
        url = reverse("readiness_check")
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["status"] == "ready"
        assert "checks" in response.data
        assert response.data["checks"]["database"]["status"] == "healthy"
        assert response.data["checks"]["cache"]["status"] == "healthy"
