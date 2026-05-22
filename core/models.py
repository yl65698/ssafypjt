from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    title = models.CharField(max_length=200)
    itad_id = models.CharField(max_length=120, blank=True)
    steam_app_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    genre = models.CharField(max_length=100, blank=True)
    release_date = models.DateField(null=True, blank=True)
    developer = models.CharField(max_length=160, blank=True)
    publisher = models.CharField(max_length=160, blank=True)
    platforms = models.CharField(max_length=255, default="Steam")
    review_score = models.PositiveSmallIntegerField(default=80)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Store(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    store_url = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GamePrice(models.Model):
    game = models.ForeignKey(Game, related_name="prices", on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name="prices", on_delete=models.CASCADE)
    current_price = models.PositiveIntegerField()
    original_price = models.PositiveIntegerField()
    discount_rate = models.PositiveSmallIntegerField(default=0)
    historical_low = models.PositiveIntegerField()
    lowest_3m = models.PositiveIntegerField()
    lowest_1y = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default="KRW")
    purchase_url = models.URLField(blank=True)
    checked_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["current_price"]

    def __str__(self):
        return f"{self.game} - {self.store}: {self.current_price}"


class GameRequirement(models.Model):
    MINIMUM = "minimum"
    RECOMMENDED = "recommended"
    REQUIREMENT_TYPES = [(MINIMUM, "Minimum"), (RECOMMENDED, "Recommended")]

    game = models.ForeignKey(Game, related_name="requirements", on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=REQUIREMENT_TYPES)
    cpu = models.CharField(max_length=120)
    gpu = models.CharField(max_length=120)
    ram_gb = models.PositiveSmallIntegerField()
    storage_gb = models.PositiveSmallIntegerField()
    os = models.CharField(max_length=120, default="Windows 10")

    class Meta:
        unique_together = ("game", "type")

    def __str__(self):
        return f"{self.game} {self.type}"


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    games = models.ManyToManyField(Game, related_name="tags", through="GameTag")

    def __str__(self):
        return self.name


class GameTag(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("game", "tag")


class UserGame(models.Model):
    STATUS_CHOICES = [
        ("wishlist", "Wishlist"),
        ("playing", "Playing"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(User, related_name="user_games", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name="user_games", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="wishlist")
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "game")


class PlayDNA(models.Model):
    user = models.OneToOneField(User, related_name="play_dna", on_delete=models.CASCADE)
    explorer_score = models.PositiveSmallIntegerField(default=0)
    story_score = models.PositiveSmallIntegerField(default=0)
    challenger_score = models.PositiveSmallIntegerField(default=0)
    strategist_score = models.PositiveSmallIntegerField(default=0)
    relaxer_score = models.PositiveSmallIntegerField(default=0)
    collector_score = models.PositiveSmallIntegerField(default=0)
    social_score = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def as_dict(self):
        return {
            "Explorer": self.explorer_score,
            "Story Lover": self.story_score,
            "Challenger": self.challenger_score,
            "Strategist": self.strategist_score,
            "Relaxer": self.relaxer_score,
            "Collector": self.collector_score,
            "Social Player": self.social_score,
        }


class UserDevice(models.Model):
    user = models.ForeignKey(User, related_name="devices", on_delete=models.CASCADE)
    cpu = models.CharField(max_length=120)
    gpu = models.CharField(max_length=120)
    ram_gb = models.PositiveSmallIntegerField()
    storage_gb = models.PositiveSmallIntegerField()
    monitor_resolution = models.CharField(max_length=40, default="FHD")
    refresh_rate = models.PositiveSmallIntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.gpu}"


class Product(models.Model):
    name = models.CharField(max_length=220)
    category = models.CharField(max_length=80)
    brand = models.CharField(max_length=80, blank=True)
    price = models.PositiveIntegerField()
    mall_name = models.CharField(max_length=120, blank=True)
    product_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    searched_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return self.name


class GearRecommendation(models.Model):
    user = models.ForeignKey(User, related_name="gear_recommendations", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name="gear_recommendations", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="gear_recommendations", on_delete=models.CASCADE)
    target_purpose = models.CharField(max_length=120)
    gear_score = models.PositiveSmallIntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
