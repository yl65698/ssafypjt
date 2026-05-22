from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .models import Game, GamePrice, Product, UserDevice


GPU_SCORES = {
    "gtx 1060": 45,
    "gtx 1660": 55,
    "rtx 2060": 62,
    "rtx 3060": 72,
    "rtx 4060": 76,
    "rtx 4070": 88,
    "rtx 4070 super": 92,
    "rtx 4080": 97,
    "rx 6600": 67,
    "rx 7600": 74,
    "rx 7800 xt": 90,
}

CPU_SCORES = {
    "i5-9400": 55,
    "i5-10400": 62,
    "i5-12400": 76,
    "i5-13400": 82,
    "i7-12700": 88,
    "ryzen 5 3600": 65,
    "ryzen 5 5600": 76,
    "ryzen 5 7600": 86,
    "ryzen 7 7700": 91,
}


def _component_score(value: str, table: dict[str, int], default: int = 60) -> int:
    normalized = value.lower()
    for key, score in table.items():
        if key in normalized:
            return score
    return default


def get_best_price(game: Game) -> GamePrice | None:
    return game.prices.order_by("current_price").first()


def buy_timing(game: Game) -> dict:
    best = get_best_price(game)
    if not best:
        return {
            "status": "WATCH",
            "score": 50,
            "reason": "가격 데이터가 부족하여 관심 목록에 넣고 추적하는 것을 추천합니다.",
        }

    historical_gap = 1 - min(best.current_price / max(best.historical_low, 1), 1.5)
    recent_gap = 1 - min(best.current_price / max(best.lowest_1y, 1), 1.5)
    discount_score = min(best.discount_rate, 80)
    low_score = max(0, int((historical_gap + 0.5) * 35))
    recent_score = max(0, int((recent_gap + 0.5) * 25))
    review_bonus = min(game.review_score // 10, 10)
    score = max(0, min(100, discount_score + low_score + recent_score + review_bonus - 20))

    if score >= 80:
        status = "BUY"
        reason = "현재가가 최근 최저가와 가깝고 할인율도 높아 구매하기 좋은 타이밍입니다."
    elif score >= 50:
        status = "WATCH"
        reason = "가격은 나쁘지 않지만 역대 최저가와 차이가 있어 추적을 추천합니다."
    else:
        status = "WAIT"
        reason = "현재 가격 매력이 낮아 다음 할인까지 기다리는 것을 추천합니다."

    return {"status": status, "score": score, "reason": reason}


def price_prediction(game: Game) -> dict:
    best = get_best_price(game)
    if not best:
        return {"days": None, "discount": None, "summary": "가격 히스토리가 부족합니다."}

    if best.discount_rate >= 50:
        days = 45
        discount = f"{best.discount_rate}~{min(best.discount_rate + 10, 80)}%"
    elif best.discount_rate >= 30:
        days = 28
        discount = f"{best.discount_rate + 10}~{min(best.discount_rate + 20, 70)}%"
    else:
        days = 18
        discount = "30~50%"

    return {
        "days": days,
        "discount": discount,
        "summary": f"약 {days}일 내 {discount} 수준의 할인이 다시 나타날 가능성이 있습니다.",
    }


def playability(game: Game, device: UserDevice | None) -> dict:
    recommended = game.requirements.filter(type="recommended").first()
    if not device or not recommended:
        return {
            "score": 0,
            "label": "장비 정보 필요",
            "summary": "보유 장비를 등록하면 실행 가능 여부를 분석할 수 있습니다.",
            "targets": [],
        }

    user_gpu = _component_score(device.gpu, GPU_SCORES)
    user_cpu = _component_score(device.cpu, CPU_SCORES)
    req_gpu = _component_score(recommended.gpu, GPU_SCORES)
    req_cpu = _component_score(recommended.cpu, CPU_SCORES)
    gpu_score = min(100, int(user_gpu / max(req_gpu, 1) * 45))
    cpu_score = min(25, int(user_cpu / max(req_cpu, 1) * 25))
    ram_score = 20 if device.ram_gb >= recommended.ram_gb else int(device.ram_gb / recommended.ram_gb * 20)
    storage_score = 10 if device.storage_gb >= recommended.storage_gb else int(device.storage_gb / recommended.storage_gb * 10)
    score = min(100, gpu_score + cpu_score + ram_score + storage_score)

    if score >= 85:
        label = "원활"
    elif score >= 70:
        label = "가능"
    elif score >= 50:
        label = "옵션 타협 필요"
    else:
        label = "업그레이드 권장"

    targets = [
        {"name": "FHD 60fps", "status": "가능" if score >= 60 else "어려움"},
        {"name": "FHD 144fps", "status": "가능" if score >= 82 else "보통" if score >= 65 else "어려움"},
        {"name": "QHD 144Hz", "status": "가능" if score >= 90 else "GPU 업그레이드 권장"},
        {"name": "4K 60fps", "status": "가능" if score >= 95 else "권장하지 않음"},
    ]
    return {
        "score": score,
        "label": label,
        "summary": f"{game.title} 권장 사양 기준으로 {label} 단계입니다.",
        "targets": targets,
    }


def recommend_products(game: Game, device: UserDevice | None, limit: int = 3) -> list[dict]:
    products = Product.objects.all()
    if device:
        current_gpu = _component_score(device.gpu, GPU_SCORES)
        if current_gpu < 85:
            products = products.filter(category__iexact="GPU")

    result = []
    for product in products[:limit]:
        score = 70
        if "4070" in product.name.lower() or "7800" in product.name.lower():
            score += 18
        if product.price < 900000:
            score += 8
        result.append(
            {
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "brand": product.brand,
                "price": product.price,
                "mall_name": product.mall_name,
                "product_url": product.product_url,
                "image_url": product.image_url,
                "gear_score": min(score, 100),
                "reason": f"{game.title}의 QHD/FHD 고주사율 환경을 목표로 할 때 가격과 성능 균형이 좋습니다.",
            }
        )
    return result


def analyze_play_dna(user) -> dict:
    scores = {
        "Explorer": 10,
        "Story Lover": 10,
        "Challenger": 10,
        "Strategist": 10,
        "Relaxer": 10,
        "Collector": 10,
        "Social Player": 10,
    }
    tag_map = {
        "Open World": "Explorer",
        "Story Rich": "Story Lover",
        "Souls-like": "Challenger",
        "Strategy": "Strategist",
        "Cozy": "Relaxer",
        "Loot": "Collector",
        "Co-op": "Social Player",
    }
    for user_game in user.user_games.select_related("game").prefetch_related("game__tags"):
        for tag in user_game.game.tags.all():
            if tag.name in tag_map:
                scores[tag_map[tag.name]] += 18
    total = sum(scores.values()) or 1
    return {key: round(value / total * 100) for key, value in scores.items()}


def natural_search(query: str) -> list[Game]:
    lowered = query.lower()
    games = Game.objects.prefetch_related("tags", "prices")
    scored = []
    for game in games:
        text = " ".join([game.title, game.genre, game.description, *[tag.name for tag in game.tags.all()]]).lower()
        score = 0
        for token in lowered.split():
            if token in text:
                score += 3
        if any(word in lowered for word in ["힐링", "편안", "cozy"]):
            score += 8 if "cozy" in text or "simulation" in text else 0
        if any(word in lowered for word in ["친구", "협동", "멀티", "co-op"]):
            score += 8 if "co-op" in text else 0
        if any(word in lowered for word in ["어려", "도전", "전투"]):
            score += 8 if "souls-like" in text or "action" in text else 0
        scored.append((score, game))
    return [game for score, game in sorted(scored, key=lambda item: item[0], reverse=True) if score > 0][:6]
