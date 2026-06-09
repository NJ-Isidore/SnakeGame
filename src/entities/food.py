"""食物系统：多种食物类型与工厂生成"""
import random
import time
from dataclasses import dataclass, field
from src.core.state import FoodType

# 各类型食物的分值
FOOD_SCORE: dict[FoodType, int] = {
    FoodType.NORMAL: 10,
    FoodType.BONUS: 30,
    FoodType.SLOW: 10,
    FoodType.GROWTH: 20,
}

# 各类型食物的生长节数
FOOD_GROWTH: dict[FoodType, int] = {
    FoodType.NORMAL: 1,
    FoodType.BONUS: 1,
    FoodType.SLOW: 1,
    FoodType.GROWTH: 2,
}

# 食物出现权重（用于随机选择）
FOOD_WEIGHTS: dict[FoodType, float] = {
    FoodType.NORMAL: 60.0,
    FoodType.BONUS: 15.0,
    FoodType.SLOW: 15.0,
    FoodType.GROWTH: 10.0,
}


@dataclass
class Food:
    """食物实体"""
    x: int
    y: int
    food_type: FoodType
    ttl_seconds: float | None = None
    _spawn_time: float = field(default=0.0, repr=False)

    def __post_init__(self):
        """创建时自动记录生成时间（仅限时食物）"""
        if self.ttl_seconds is not None:
            self._spawn_time = time.time()

    @property
    def pos(self) -> tuple[int, int]:
        """返回坐标元组"""
        return (self.x, self.y)

    @property
    def score(self) -> int:
        """返回分值"""
        return FOOD_SCORE[self.food_type]

    @property
    def growth(self) -> int:
        """返回生长节数"""
        return FOOD_GROWTH[self.food_type]

    def is_expired(self, current_time: float) -> bool:
        """检查食物是否过期"""
        if self.ttl_seconds is None:
            return False
        return (current_time - self._spawn_time) > self.ttl_seconds


class FoodFactory:
    """食物工厂：在网格中随机生成食物"""

    def __init__(self, grid_cols: int = 20, grid_rows: int = 20):
        self._cols = grid_cols
        self._rows = grid_rows

    def spawn(
        self,
        occupied: set[tuple[int, int]],
        forced_type: FoodType | None = None,
    ) -> Food:
        """在可用位置生成一个食物"""
        available = [
            (x, y)
            for x in range(self._cols)
            for y in range(self._rows)
            if (x, y) not in occupied
        ]
        if not available:
            raise ValueError("没有可用位置放置食物")

        pos = random.choice(available)
        food_type = forced_type or self._random_type()

        ttl = 8.0 if food_type == FoodType.BONUS else None
        return Food(
            x=pos[0], y=pos[1],
            food_type=food_type,
            ttl_seconds=ttl,
        )

    def _random_type(self) -> FoodType:
        """按权重随机选择食物类型"""
        types = list(FOOD_WEIGHTS.keys())
        weights = list(FOOD_WEIGHTS.values())
        return random.choices(types, weights=weights, k=1)[0]
