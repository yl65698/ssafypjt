from django.contrib import admin

from .models import (
    Game,
    GamePrice,
    GameRequirement,
    GearRecommendation,
    Product,
    Store,
    Tag,
    UserDevice,
    UserGame,
)


admin.site.register(Game)
admin.site.register(Store)
admin.site.register(GamePrice)
admin.site.register(GameRequirement)
admin.site.register(Tag)
admin.site.register(UserGame)
admin.site.register(UserDevice)
admin.site.register(Product)
admin.site.register(GearRecommendation)

# Register your models here.
