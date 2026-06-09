"""障碍物管理：生成、存储和查询障碍物"""
import random


class ObstacleManager:
    """障碍物管理器：管理网格中的障碍物"""

    def __init__(self, grid_cols: int = 20, grid_rows: int = 20):
        self._cols = grid_cols
        self._rows = grid_rows
        self._positions: set[tuple[int, int]] = set()

    @property
    def count(self) -> int:
        """返回障碍物数量"""
        return len(self._positions)

    @property
    def all_positions(self) -> set[tuple[int, int]]:
        """返回所有障碍物位置的副本"""
        return set(self._positions)

    def occupies(self, pos: tuple[int, int]) -> bool:
        """检查指定位置是否有障碍物"""
        return pos in self._positions

    def generate(
        self,
        count: int,
        occupied: set[tuple[int, int]],
    ) -> None:
        """在可用位置生成指定数量的障碍物"""
        available = [
            (x, y)
            for x in range(self._cols)
            for y in range(self._rows)
            if (x, y) not in occupied and (x, y) not in self._positions
        ]
        to_place = min(count, len(available))
        chosen = random.sample(available, to_place)
        self._positions.update(chosen)

    def clear(self) -> None:
        """清除所有障碍物"""
        self._positions.clear()
