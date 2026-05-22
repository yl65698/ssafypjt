from django.core.management import call_command
from django.test import Client, TestCase

from .models import Game


class VrseApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_vrse", verbosity=0)

    def test_dashboard_returns_sections(self):
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("buy_now", response.json())

    def test_game_detail_contains_buy_status(self):
        game = Game.objects.first()
        response = self.client.get(f"/api/games/{game.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("buy_status", response.json())

    def test_natural_search_finds_coop_game(self):
        response = self.client.post(
            "/api/games/natural-search/",
            data={"query": "친구랑 협동 게임"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        titles = [game["title"] for game in response.json()]
        self.assertIn("It Takes Two", titles)

# Create your tests here.
