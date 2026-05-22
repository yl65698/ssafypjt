from datetime import date

from django.core.management.base import BaseCommand

from core.models import Game, GamePrice, GameRequirement, GameTag, Product, Store, Tag


class Command(BaseCommand):
    help = "Create VRSE demo data"

    def handle(self, *args, **options):
        stores = {
            "steam": Store.objects.get_or_create(
                slug="steam",
                defaults={"name": "Steam", "store_url": "https://store.steampowered.com/"},
            )[0],
            "humble": Store.objects.get_or_create(
                slug="humble",
                defaults={"name": "Humble Store", "store_url": "https://www.humblebundle.com/store"},
            )[0],
            "epic": Store.objects.get_or_create(
                slug="epic",
                defaults={"name": "Epic Games", "store_url": "https://store.epicgames.com/"},
            )[0],
        }

        games = [
            {
                "title": "Elden Ring",
                "genre": "Open World RPG",
                "description": "광활한 오픈월드와 강렬한 전투가 중심인 액션 RPG입니다.",
                "image_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/header.jpg",
                "release_date": date(2022, 2, 25),
                "developer": "FromSoftware",
                "publisher": "Bandai Namco",
                "review_score": 94,
                "tags": ["Open World", "Souls-like", "Action", "Fantasy"],
                "req": ("i5-8400", "GTX 1060", 12, 60),
                "prices": [(39000, 64800, 40, 33000, 39000, 36000), (42000, 64800, 35, 33000, 39000, 36000)],
            },
            {
                "title": "Stardew Valley",
                "genre": "Simulation",
                "description": "농장, 낚시, 마을 생활을 즐기는 따뜻한 생활 시뮬레이션 게임입니다.",
                "image_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/413150/header.jpg",
                "release_date": date(2016, 2, 26),
                "developer": "ConcernedApe",
                "publisher": "ConcernedApe",
                "review_score": 98,
                "tags": ["Cozy", "Simulation", "Co-op", "Relaxing"],
                "req": ("i5-9400", "GTX 1060", 4, 1),
                "prices": [(8400, 16000, 48, 6800, 8400, 7600), (9000, 16000, 44, 6800, 8400, 7600)],
            },
            {
                "title": "It Takes Two",
                "genre": "Co-op Adventure",
                "description": "두 명이 함께 퍼즐과 액션을 해결하는 협동 어드벤처 게임입니다.",
                "image_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1426210/header.jpg",
                "release_date": date(2021, 3, 26),
                "developer": "Hazelight",
                "publisher": "Electronic Arts",
                "review_score": 95,
                "tags": ["Co-op", "Story Rich", "Adventure", "Family Friendly"],
                "req": ("i5-3570K", "GTX 980", 16, 50),
                "prices": [(19800, 44000, 55, 13200, 19800, 17600), (22000, 44000, 50, 13200, 19800, 17600)],
            },
            {
                "title": "Cyberpunk 2077",
                "genre": "RPG",
                "description": "네온 도시 나이트시티에서 펼쳐지는 몰입형 오픈월드 RPG입니다.",
                "image_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/header.jpg",
                "release_date": date(2020, 12, 10),
                "developer": "CD PROJEKT RED",
                "publisher": "CD PROJEKT RED",
                "review_score": 86,
                "tags": ["Open World", "Story Rich", "RPG", "Sci-fi"],
                "req": ("i7-12700", "RTX 2060", 16, 70),
                "prices": [(33000, 66000, 50, 22000, 33000, 28600), (35000, 66000, 47, 22000, 33000, 28600)],
            },
            {
                "title": "Hades",
                "genre": "Roguelike Action",
                "description": "빠른 전투와 반복 플레이가 매력적인 로그라이크 액션 게임입니다.",
                "image_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1145360/header.jpg",
                "release_date": date(2020, 9, 17),
                "developer": "Supergiant Games",
                "publisher": "Supergiant Games",
                "review_score": 98,
                "tags": ["Action", "Story Rich", "Challenger", "Loot"],
                "req": ("i5-9400", "GTX 1060", 8, 15),
                "prices": [(12500, 27000, 54, 9900, 12500, 11000), (13000, 27000, 52, 9900, 12500, 11000)],
            },
            {
                "title": "Civilization VI",
                "genre": "Strategy",
                "description": "문명을 성장시키고 세계를 경영하는 턴제 전략 게임입니다.",
                "image_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/289070/header.jpg",
                "release_date": date(2016, 10, 21),
                "developer": "Firaxis Games",
                "publisher": "2K",
                "review_score": 88,
                "tags": ["Strategy", "Simulation", "Turn-Based", "Management"],
                "req": ("i5-9400", "GTX 1060", 8, 23),
                "prices": [(6500, 65000, 90, 6500, 6500, 6500), (7200, 65000, 89, 6500, 6500, 6500)],
            },
        ]

        for index, data in enumerate(games):
            game, _ = Game.objects.update_or_create(
                title=data["title"],
                defaults={
                    "itad_id": data["title"].lower().replace(" ", "-"),
                    "steam_app_id": 100000 + index,
                    "genre": data["genre"],
                    "description": data["description"],
                    "image_url": data["image_url"],
                    "release_date": data["release_date"],
                    "developer": data["developer"],
                    "publisher": data["publisher"],
                    "platforms": "Steam, Epic, Humble",
                    "review_score": data["review_score"],
                },
            )
            GameRequirement.objects.update_or_create(
                game=game,
                type="recommended",
                defaults={
                    "cpu": data["req"][0],
                    "gpu": data["req"][1],
                    "ram_gb": data["req"][2],
                    "storage_gb": data["req"][3],
                },
            )
            GameRequirement.objects.update_or_create(
                game=game,
                type="minimum",
                defaults={
                    "cpu": "i5-9400",
                    "gpu": "GTX 1060",
                    "ram_gb": max(4, data["req"][2] // 2),
                    "storage_gb": data["req"][3],
                },
            )
            for tag_name in data["tags"]:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                GameTag.objects.get_or_create(game=game, tag=tag)
            for store, price_data in zip(stores.values(), data["prices"]):
                GamePrice.objects.update_or_create(
                    game=game,
                    store=store,
                    defaults={
                        "current_price": price_data[0],
                        "original_price": price_data[1],
                        "discount_rate": price_data[2],
                        "historical_low": price_data[3],
                        "lowest_3m": price_data[4],
                        "lowest_1y": price_data[5],
                        "purchase_url": store.store_url,
                    },
                )

        products = [
            ("RTX 4070 SUPER 12GB", "GPU", "NVIDIA", 890000, "Naver Shopping"),
            ("RTX 4070 12GB", "GPU", "NVIDIA", 780000, "Naver Shopping"),
            ("RX 7800 XT 16GB", "GPU", "AMD", 760000, "Naver Shopping"),
            ("Ryzen 5 7600", "CPU", "AMD", 260000, "Naver Shopping"),
            ("Intel i5-13400F", "CPU", "Intel", 245000, "Naver Shopping"),
            ("QHD 144Hz Gaming Monitor", "모니터", "LG", 360000, "Naver Shopping"),
            ("Mechanical Gaming Keyboard", "키보드", "Logitech", 129000, "Naver Shopping"),
            ("Wireless Gaming Headset", "헤드셋", "SteelSeries", 149000, "Naver Shopping"),
        ]
        for name, category, brand, price, mall in products:
            Product.objects.update_or_create(
                name=name,
                defaults={
                    "category": category,
                    "brand": brand,
                    "price": price,
                    "mall_name": mall,
                    "product_url": "https://search.shopping.naver.com/search/all?query=" + name.replace(" ", "%20"),
                    "image_url": "https://placehold.co/640x360/22262e/f4f1e8?text=" + name.replace(" ", "+"),
                },
            )

        self.stdout.write(self.style.SUCCESS("VRSE demo data is ready."))
