"""测试难度管理"""
from src.systems.difficulty import DifficultyManager


def test_initial_level():
    """测试初始等级"""
    mgr = DifficultyManager()
    assert mgr.level == 1
    assert mgr.speed == 8


def test_level_up():
    """测试升级"""
    mgr = DifficultyManager()
    mgr.check_level_up(score=50)
    assert mgr.level == 2
    assert mgr.speed == 9


def test_multiple_level_ups():
    """测试多次升级"""
    mgr = DifficultyManager()
    mgr.check_level_up(score=150)
    assert mgr.level == 4
    assert mgr.speed == 11


def test_speed_cap():
    """测试速度上限"""
    mgr = DifficultyManager(max_speed=12)
    mgr.check_level_up(score=1000)
    assert mgr.speed <= 12


def test_obstacle_count_for_level():
    """测试各等级障碍物数量"""
    mgr = DifficultyManager()
    assert mgr.obstacle_count_for_level(1) == 0
    assert mgr.obstacle_count_for_level(2) == 3
    assert mgr.obstacle_count_for_level(3) == 6


def test_apply_slow_effect():
    """测试减速效果"""
    mgr = DifficultyManager()
    mgr.check_level_up(score=100)  # level 3, speed 10
    original_speed = mgr.speed
    mgr.apply_slow(duration=5.0, current_time=0.0)
    assert mgr.speed == original_speed - 2
    # 效果过期后恢复
    mgr.update_effects(current_time=6.0)
    assert mgr.speed == original_speed
