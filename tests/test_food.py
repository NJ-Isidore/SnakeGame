"""测试食物系统"""
import pytest
from src.entities.food import Food, FoodFactory, FOOD_SCORE
from src.core.state import FoodType


def test_food_position():
    """测试食物位置"""
    food = Food(x=5, y=5, food_type=FoodType.NORMAL)
    assert food.pos == (5, 5)


def test_food_score_values():
    """测试食物分值"""
    assert FOOD_SCORE[FoodType.NORMAL] == 10
    assert FOOD_SCORE[FoodType.BONUS] == 30
    assert FOOD_SCORE[FoodType.SLOW] == 10
    assert FOOD_SCORE[FoodType.GROWTH] == 20


def test_food_factory_creates_normal():
    """测试工厂创建普通食物"""
    factory = FoodFactory(grid_cols=20, grid_rows=20)
    occupied = {(10, 10), (9, 10)}
    food = factory.spawn(occupied, forced_type=FoodType.NORMAL)
    assert food.food_type == FoodType.NORMAL
    assert food.pos not in occupied


def test_food_factory_avoids_occupied():
    """测试工厂避开已占据位置"""
    factory = FoodFactory(grid_cols=3, grid_rows=3)
    # 占据除 (0,0) 外的所有位置
    occupied = {(x, y) for x in range(3) for y in range(3) if (x, y) != (0, 0)}
    food = factory.spawn(occupied, forced_type=FoodType.NORMAL)
    assert food.pos == (0, 0)


def test_bonus_food_has_ttl():
    """测试奖励食物有时限"""
    food = Food(x=1, y=1, food_type=FoodType.BONUS, ttl_seconds=5.0)
    # 刚创建时不应过期
    import time
    assert food.is_expired(time.time()) is False
    # 超过 TTL 后应过期
    assert food.is_expired(time.time() + 6.0) is True


def test_normal_food_no_ttl():
    """测试普通食物无时限"""
    food = Food(x=1, y=1, food_type=FoodType.NORMAL)
    assert food.is_expired(100.0) is False
