from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Game, GamePrice, GameRequirement, Product, Store, Tag, UserDevice, UserGame
from .services import buy_timing, get_best_price, price_prediction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "slug", "store_url"]


class GamePriceSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)

    class Meta:
        model = GamePrice
        fields = [
            "id",
            "store",
            "current_price",
            "original_price",
            "discount_rate",
            "historical_low",
            "lowest_3m",
            "lowest_1y",
            "currency",
            "purchase_url",
            "checked_at",
        ]


class GameRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRequirement
        fields = ["id", "type", "cpu", "gpu", "ram_gb", "storage_gb", "os"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class GameListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    best_price = serializers.SerializerMethodField()
    buy_status = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "description",
            "image_url",
            "genre",
            "platforms",
            "review_score",
            "tags",
            "best_price",
            "buy_status",
        ]

    def get_best_price(self, obj):
        price = get_best_price(obj)
        return GamePriceSerializer(price).data if price else None

    def get_buy_status(self, obj):
        return buy_timing(obj)


class GameDetailSerializer(GameListSerializer):
    prices = GamePriceSerializer(many=True, read_only=True)
    requirements = GameRequirementSerializer(many=True, read_only=True)
    price_prediction = serializers.SerializerMethodField()

    class Meta(GameListSerializer.Meta):
        fields = GameListSerializer.Meta.fields + [
            "itad_id",
            "steam_app_id",
            "release_date",
            "developer",
            "publisher",
            "prices",
            "requirements",
            "price_prediction",
        ]

    def get_price_prediction(self, obj):
        return price_prediction(obj)


class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = [
            "id",
            "cpu",
            "gpu",
            "ram_gb",
            "storage_gb",
            "monitor_resolution",
            "refresh_rate",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category", "brand", "price", "mall_name", "product_url", "image_url"]


class UserGameSerializer(serializers.ModelSerializer):
    game = GameListSerializer(read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(source="game", queryset=Game.objects.all(), write_only=True)

    class Meta:
        model = UserGame
        fields = ["id", "game", "game_id", "status", "rating", "is_favorite", "created_at"]
        read_only_fields = ["id", "created_at"]
