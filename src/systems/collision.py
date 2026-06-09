"""碰撞检测系统"""
from src.entities.snake import Snake
from src.entities.food import Food
from src.entities.obstacle import ObstacleManager


class CollisionDetector:
    """碰撞检测器：检测蛇与墙壁、自身、食物、障碍物的碰撞"""

    def __init__(self, grid_cols: int = 20, grid_rows: int = 20):
        self._cols = grid_cols
        self._rows = grid_rows

    def hits_wall(self, snake: Snake) -> bool:
        """检测蛇是否撞墙"""
        hx, hy = snake.head.pos
        return hx < 0 or hx >= self._cols or hy < 0 or hy >= self._rows

    def hits_self(self, snake: Snake) -> bool:
        """检测蛇是否撞到自己"""
        head_pos = snake.head.pos
        return head_pos in snake.body_positions

    def hits_food(self, snake: Snake, food: Food) -> bool:
        """检测蛇是否吃到食物"""
        return snake.head.pos == food.pos

    def hits_obstacle(self, snake: Snake, obstacles: ObstacleManager) -> bool:
        """检测蛇是否撞到障碍物"""
        return obstacles.occupies(snake.head.pos)
