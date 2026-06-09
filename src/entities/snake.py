"""蛇实体：管理蛇的状态、移动和生长"""
from dataclasses import dataclass, field
from src.core.state import Direction


@dataclass
class SnakeSegment:
    """蛇的一个节段"""
    x: int
    y: int

    @property
    def pos(self) -> tuple[int, int]:
        """返回坐标元组"""
        return (self.x, self.y)


class Snake:
    """蛇：由多个节段组成，支持移动、生长和方向缓冲"""

    def __init__(self, start_pos: tuple[int, int] = (10, 10)):
        sx, sy = start_pos
        # 初始 3 节：头 + 2 节身体，默认朝右
        self.segments: list[SnakeSegment] = [
            SnakeSegment(sx, sy),
            SnakeSegment(sx - 1, sy),
            SnakeSegment(sx - 2, sy),
        ]
        self._direction: Direction = Direction.RIGHT
        self._direction_buffer: list[Direction] = []
        self._pending_growth: int = 0

    @property
    def head(self) -> SnakeSegment:
        """返回蛇头"""
        return self.segments[0]

    @property
    def direction(self) -> Direction:
        """返回当前方向"""
        return self._direction

    @direction.setter
    def direction(self, new_dir: Direction) -> None:
        """设置方向，禁止直接反向"""
        if new_dir != self._direction.opposite:
            self._direction = new_dir

    def set_direction(self, new_dir: Direction) -> None:
        """缓冲方向输入，防止快速按键导致反向"""
        if self._direction_buffer:
            last = self._direction_buffer[-1]
        else:
            last = self._direction
        if new_dir != last.opposite and new_dir != last:
            self._direction_buffer.append(new_dir)

    def move(self) -> None:
        """移动蛇：先应用缓冲方向，再移动一格"""
        if self._direction_buffer:
            next_dir = self._direction_buffer.pop(0)
            if next_dir != self._direction.opposite:
                self._direction = next_dir

        dx, dy = self._direction.value
        new_head = SnakeSegment(
            self.head.x + dx,
            self.head.y + dy,
        )
        self.segments.insert(0, new_head)

        # 如果有待生长量，不移除尾部
        if self._pending_growth > 0:
            self._pending_growth -= 1
        else:
            self.segments.pop()

    def grow(self, amount: int = 1) -> None:
        """生长指定节数"""
        self._pending_growth += amount

    def occupies(self, pos: tuple[int, int]) -> bool:
        """检查蛇是否占据指定位置"""
        return any(seg.pos == pos for seg in self.segments)

    @property
    def body_positions(self) -> list[tuple[int, int]]:
        """返回除蛇头外的所有身体位置（用于自碰撞检测）"""
        return [seg.pos for seg in self.segments[1:]]
