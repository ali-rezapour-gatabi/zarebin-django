from .views.idea_view import IdeasViewSet
from .views.vots_view import CommentsViewSet, VotesViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"ideas", IdeasViewSet, basename="ideas")
router.register(r"comments", CommentsViewSet, basename="comments")
router.register(r"votes", VotesViewSet, basename="votes")

urlpatterns = [
    path("", include(router.urls)),
]
