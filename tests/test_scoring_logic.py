from app.core.scoring import ScoringService, validate_profile_blocks


def test_single_red_profile():
    scores = {"red": 72, "yellow": 57, "green": 48, "blue": 42}
    info = ScoringService.get_profile_key(scores)
    result = ScoringService.generate_result(scores)

    assert info["profile_type"] == "single"
    assert info["profile_key"] == "red"
    assert info["primary_style"] == "red"
    assert info["secondary_style"] == "yellow"
    assert info["lowest_style"] == "blue"
    assert info["difference"] == 15
    assert "🔴 Красный — Драйвер / Результат" in result
    assert "Если разница между двумя ведущими стилями" not in result
    assert "profile_key" not in result
    assert "difference" not in result


def test_mixed_red_yellow_profile():
    scores = {"red": 65, "yellow": 60, "blue": 50, "green": 25}
    info = ScoringService.get_profile_key(scores)
    result = ScoringService.generate_result(scores)

    assert info["profile_type"] == "mixed"
    assert info["profile_key"] == "red_yellow"
    assert info["primary_style"] == "red"
    assert info["secondary_style"] == "yellow"
    assert info["lowest_style"] == "green"
    assert info["difference"] == 5
    assert "🔴🟡 Драйвер-вдохновитель" in result
    assert "Красный профиль" not in result
    assert "Если разница между двумя ведущими стилями" not in result


def test_mixed_order_matters():
    scores = {"yellow": 70, "red": 65, "green": 40, "blue": 35}
    info = ScoringService.get_profile_key(scores)
    result = ScoringService.generate_result(scores)

    assert info["profile_type"] == "mixed"
    assert info["profile_key"] == "yellow_red"
    assert info["profile_key"] != "red_yellow"
    assert "🟡🔴 Энергичный инициатор" in result


def test_lowest_style_attention_zone():
    scores = {"blue": 80, "green": 72, "red": 45, "yellow": 30}
    info = ScoringService.get_profile_key(scores)
    result = ScoringService.generate_result(scores)

    assert info["profile_type"] == "mixed"
    assert info["profile_key"] == "blue_green"
    assert info["lowest_style"] == "yellow"
    assert "<b>Зона внимания</b>" in result


def test_all_profile_blocks_are_complete():
    validate_profile_blocks()
    scores = {"red": 65, "yellow": 60, "blue": 50, "green": 25}
    for context in ("sales", "management", "team", "communication", "stress", "advice"):
        assert ScoringService.generate_context_result(scores, context)
