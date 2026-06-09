"""难度管理：速度递增、等级、减速效果"""
from src.core.state import INITIAL_SPEED, MAX_SPEED, SPEED_INCREMENT, SCORE_PER_LEVEL


class DifficultyManager:
    """难度管理器：管理游戏难度、速度和减速效果"""

    def __init__(
        self,
        initial_speed: int = INITIAL_SPEED,
        max_speed: int = MAX_SPEED,
        score_per_level: int = SCORE_PER_LEVEL,
    ):
        self._initial_speed = initial_speed
        self._max_speed = max_speed
        self._score_per_level = score_per_level
        self._level: int = 1
        self._speed: int = initial_speed
        self._slow_until: float = 0.0
        self._slow_amount: int = 2

    @property
    def level(self) -> int:
        """返回当前等级"""
        return self._level

    @property
    def speed(self) -> int:
        """返回当前速度"""
        return self._speed

    def check_level_up(self, score: int) -> None:
        """根据分数检查并执行升级"""
        new_level = (score // self._score_per_level) + 1
        if new_level > self._level:
            self._level = new_level
            base_speed = self._initial_speed + (self._level - 1) * SPEED_INCREMENT
            self._speed = min(base_speed, self._max_speed)
            self._apply_slow_if_active()

    def obstacle_count_for_level(self, level: int) -> int:
        """返回指定等级应有的障碍物数量"""
        if level < 2:
            return 0
        return (level - 1) * 3

    def apply_slow(self, duration: float, current_time: float) -> None:
        """应用减速效果"""
        self._slow_until = current_time + duration
        self._apply_slow_if_active()

    def update_effects(self, current_time: float) -> None:
        """更新效果状态，过期后恢复速度"""
        if current_time >= self._slow_until and self._slow_until > 0:
            self._slow_until = 0.0
            base_speed = self._initial_speed + (self._level - 1) * SPEED_INCREMENT
            self._speed = min(base_speed, self._max_speed)

    def _apply_slow_if_active(self) -> None:
        """如果减速效果激活中，应用减速"""
        if self._slow_until > 0:
            base_speed = self._initial_speed + (self._level - 1) * SPEED_INCREMENT
            base_speed = min(base_speed, self._max_speed)
            self._speed = max(self._initial_speed, base_speed - self._slow_amount)

    def reset(self) -> None:
        """重置难度到初始状态"""
        self._level = 1
        self._speed = self._initial_speed
        self._slow_until = 0.0
