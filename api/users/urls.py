from rest_framework.routers import SimpleRouter

from api.users.viewsets import UserViewSet

router = SimpleRouter("users", UserViewSet)

urlpatterns = router.urls
