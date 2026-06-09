"""测试计分系统"""
import json
import os
import tempfile
from src.systems.scoring import ScoringSystem, ScoreEntry


def test_initial_score():
    """测试初始分数"""
    scoring = ScoringSystem()
    assert scoring.score == 0
    assert scoring.combo == 0


def test_add_score_normal_food():
    """测试普通食物得分"""
    scoring = ScoringSystem()
    points = scoring.add_score(base_points=10)
    assert scoring.score == 10
    assert points == 10


def test_combo_increments():
    """测试连击递增"""
    scoring = ScoringSystem()
    scoring.add_score(10)
    scoring.add_score(10)
    assert scoring.combo == 2


def test_combo_multiplier():
    """测试连击倍率"""
    scoring = ScoringSystem()
    scoring.add_score(10)  # combo=1, 得分=10
    points = scoring.add_score(10)  # combo=2, 得分=10*2=20
    assert points == 20
    assert scoring.score == 30


def test_reset_combo():
    """测试重置连击"""
    scoring = ScoringSystem()
    scoring.add_score(10)
    scoring.add_score(10)
    scoring.reset_combo()
    assert scoring.combo == 0


def test_save_and_load_leaderboard():
    """测试保存和加载排行榜"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        temp_path = f.name

    try:
        scoring = ScoringSystem(leaderboard_path=temp_path)
        scoring.add_score(100)
        scoring.save_to_leaderboard("Player1")

        loaded = ScoringSystem(leaderboard_path=temp_path)
        entries = loaded.get_leaderboard()
        assert len(entries) == 1
        assert entries[0].name == "Player1"
        assert entries[0].score == 100
    finally:
        os.unlink(temp_path)


def test_leaderboard_sorted_descending():
    """测试排行榜按分数降序排列"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        temp_path = f.name

    try:
        scoring = ScoringSystem(leaderboard_path=temp_path)
        scoring.add_score(50)
        scoring.save_to_leaderboard("A")
        scoring._score = 0
        scoring._combo = 0
        scoring.add_score(200)
        scoring.save_to_leaderboard("B")

        entries = scoring.get_leaderboard()
        assert entries[0].score >= entries[1].score
    finally:
        os.unlink(temp_path)


def test_leaderboard_max_10():
    """测试排行榜最多10条记录"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        temp_path = f.name

    try:
        scoring = ScoringSystem(leaderboard_path=temp_path)
        for i in range(15):
            scoring._score = (i + 1) * 10
            scoring.save_to_leaderboard(f"P{i}")
        entries = scoring.get_leaderboard()
        assert len(entries) <= 10
    finally:
        os.unlink(temp_path)
