"""测试蛇实体"""
import pytest
from src.entities.snake import Snake, SnakeSegment
from src.core.state import Direction


def test_snake_initial_segments():
    """测试蛇的初始节段"""
    snake = Snake(start_pos=(10, 10))
    assert len(snake.segments) == 3
    assert snake.segments[0].pos == (10, 10)
    assert snake.segments[1].pos == (9, 10)
    assert snake.segments[2].pos == (8, 10)


def test_snake_head_property():
    """测试蛇头属性"""
    snake = Snake(start_pos=(5, 5))
    assert snake.head.pos == (5, 5)


def test_snake_move_right():
    """测试蛇向右移动"""
    snake = Snake(start_pos=(5, 5))
    snake.direction = Direction.RIGHT
    snake.move()
    assert snake.head.pos == (6, 5)


def test_snake_move_up():
    """测试蛇向上移动"""
    snake = Snake(start_pos=(5, 5))
    snake.direction = Direction.UP
    snake.move()
    assert snake.head.pos == (5, 4)


def test_cannot_reverse_direction():
    """测试不能直接反向"""
    snake = Snake(start_pos=(5, 5))
    snake.direction = Direction.RIGHT
    snake.direction = Direction.LEFT  # 尝试反向
    assert snake.direction == Direction.RIGHT


def test_snake_grow():
    """测试蛇生长"""
    snake = Snake(start_pos=(10, 10))
    initial_len = len(snake.segments)
    snake.grow()
    snake.move()
    assert len(snake.segments) == initial_len + 1


def test_snake_grow_multiple():
    """测试蛇多次生长"""
    snake = Snake(start_pos=(10, 10))
    initial_len = len(snake.segments)
    snake.grow()
    snake.grow()
    # 每次 move 应用一次生长，需要移动 2 次
    snake.move()
    snake.move()
    assert len(snake.segments) == initial_len + 2


def test_snake_occupies():
    """测试蛇占据位置检测"""
    snake = Snake(start_pos=(10, 10))
    assert snake.occupies((10, 10))
    assert snake.occupies((9, 10))
    assert not snake.occupies((0, 0))


def test_direction_buffer_prevents_rapid_reverse():
    """测试方向缓冲防止快速反向"""
    snake = Snake(start_pos=(5, 5))
    snake.direction = Direction.RIGHT
    snake.set_direction(Direction.UP)  # 缓冲
    # 第一次 move 应用 UP
    snake.move()
    assert snake.direction == Direction.UP
