from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("games", views.GameViewSet, basename="games")
router.register("products", views.ProductViewSet, basename="products")
router.register("me/devices", views.UserDeviceViewSet, basename="devices")
router.register("me/games", views.UserGameViewSet, basename="user-games")

urlpatterns = [
    path("accounts/signup/", views.signup_view),
    path("accounts/login/", views.login_view),
    path("accounts/logout/", views.logout_view),
    path("accounts/me/", views.me_view),
    path("dashboard/", views.dashboard_view),
    path("games/natural-search/", views.natural_search_view),
    path("games/<int:pk>/playability/", views.game_playability_view),
    path("games/<int:pk>/gear-recommendations/", views.gear_recommendations_view),
    path("me/play-dna/", views.play_dna_view),
    path("", include(router.urls)),
]
