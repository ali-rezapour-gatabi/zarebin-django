from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenBlacklistView
from .views import UsersViewSet

router = DefaultRouter()
router.register(r"identity", UsersViewSet, basename="identity")

urlpatterns = [
    path("", include(router.urls)),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
