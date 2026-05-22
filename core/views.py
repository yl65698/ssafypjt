from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Game, Product, UserDevice, UserGame
from .serializers import (
    GameDetailSerializer,
    GameListSerializer,
    ProductSerializer,
    UserDeviceSerializer,
    UserGameSerializer,
    UserSerializer,
)
from .services import analyze_play_dna, natural_search, playability, recommend_products


def index(request):
    return render(request, "core/index.html")


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    email = request.data.get("email", "").strip()
    password = request.data.get("password", "")
    nickname = request.data.get("nickname", "").strip() or email.split("@")[0]
    if not email or not password:
        return Response({"detail": "email과 password가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=email).exists():
        return Response({"detail": "이미 가입된 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=email, email=email, password=password, first_name=nickname)
    login(request, user)
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email", "").strip()
    password = request.data.get("password", "")
    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({"detail": "이메일 또는 비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
    login(request, user)
    return Response(UserSerializer(user).data)


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"detail": "로그아웃되었습니다."})


@api_view(["GET"])
@permission_classes([AllowAny])
def me_view(request):
    if not request.user.is_authenticated:
        return Response({"is_authenticated": False})
    return Response({"is_authenticated": True, "user": UserSerializer(request.user).data})


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.prefetch_related("tags", "prices__store", "requirements").all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GameDetailSerializer
        return GameListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get("q", "").strip()
        genre = self.request.query_params.get("genre", "").strip()
        platform = self.request.query_params.get("platform", "").strip()
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(tags__name__icontains=keyword)
            ).distinct()
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if platform:
            queryset = queryset.filter(platforms__icontains=platform)
        return queryset


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get("q", "").strip()
        category = self.request.query_params.get("category", "").strip()
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(brand__icontains=keyword))
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset


class UserDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = UserDeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserGameViewSet(viewsets.ModelViewSet):
    serializer_class = UserGameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserGame.objects.filter(user=self.request.user).select_related("game").prefetch_related("game__tags")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
@permission_classes([AllowAny])
def natural_search_view(request):
    query = request.data.get("query", "")
    games = natural_search(query)
    return Response(GameListSerializer(games, many=True).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def game_playability_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    device = None
    if request.user.is_authenticated:
        device = request.user.devices.order_by("-created_at").first()
    return Response(playability(game, device))


@api_view(["GET"])
@permission_classes([AllowAny])
def gear_recommendations_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    device = request.user.devices.order_by("-created_at").first() if request.user.is_authenticated else None
    return Response(recommend_products(game, device))


@api_view(["GET", "POST"])
def play_dna_view(request):
    scores = analyze_play_dna(request.user)
    return Response({"scores": scores})


@api_view(["GET"])
@permission_classes([AllowAny])
def dashboard_view(request):
    games = Game.objects.prefetch_related("tags", "prices__store").all()
    serialized = GameListSerializer(games[:8], many=True).data
    buy_now = sorted(serialized, key=lambda item: item["buy_status"]["score"], reverse=True)[:4]
    high_discount = sorted(
        serialized,
        key=lambda item: item["best_price"]["discount_rate"] if item["best_price"] else 0,
        reverse=True,
    )[:4]
    return Response(
        {
            "recommended": serialized[:4],
            "buy_now": buy_now,
            "high_discount": high_discount,
        }
    )
