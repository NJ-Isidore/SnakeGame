"""游戏区域渲染器：绘制网格、蛇、食物、障碍物"""
import pygame
from src.core.state import (
    GRID_COLS, GRID_ROWS, CELL_SIZE,
    GAME_WIDTH, GAME_HEIGHT,
)
from src.entities.snake import Snake
from src.entities.food import Food
from src.entities.obstacle import ObstacleManager


class Renderer:
    """游戏区域渲染器：负责绘制游戏画面"""

    def __init__(self, skin_manager):
        self._skin_mgr = skin_manager

    def draw_background(
        self, screen: pygame.Surface, skin_id: str
    ) -> None:
        """绘制背景和网格线"""
        bg = self._skin_mgr.get_color(skin_id, "background")
        screen.fill(bg, (0, 0, GAME_WIDTH, GAME_HEIGHT))
        grid_color = self._skin_mgr.get_color(skin_id, "grid_line")
        for x in range(GRID_COLS + 1):
            px = x * CELL_SIZE
            pygame.draw.line(screen, grid_color, (px, 0), (px, GAME_HEIGHT))
        for y in range(GRID_ROWS + 1):
            py = y * CELL_SIZE
            pygame.draw.line(screen, grid_color, (0, py), (GAME_WIDTH, py))

    def draw_snake(
        self, screen: pygame.Surface, snake: Snake, skin_id: str
    ) -> None:
        """绘制蛇"""
        head_color = self._skin_mgr.get_color(skin_id, "snake_head")
        body_color = self._skin_mgr.get_color(skin_id, "snake_body")
        for i, seg in enumerate(snake.segments):
            color = head_color if i == 0 else body_color
            rect = pygame.Rect(
                seg.x * CELL_SIZE + 1,
                seg.y * CELL_SIZE + 1,
                CELL_SIZE - 2,
                CELL_SIZE - 2,
            )
            pygame.draw.rect(screen, color, rect, border_radius=4)

    def draw_food(
        self, screen: pygame.Surface, food: Food, skin_id: str
    ) -> None:
        """绘制食物"""
        color_key = f"food_{food.food_type.value}"
        color = self._skin_mgr.get_color(skin_id, color_key)
        cx = food.x * CELL_SIZE + CELL_SIZE // 2
        cy = food.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(screen, color, (cx, cy), radius)

    def draw_obstacles(
        self, screen: pygame.Surface,
        obstacles: ObstacleManager, skin_id: str,
    ) -> None:
        """绘制障碍物"""
        color = self._skin_mgr.get_color(skin_id, "obstacle")
        for (ox, oy) in obstacles.all_positions:
            rect = pygame.Rect(
                ox * CELL_SIZE, oy * CELL_SIZE,
                CELL_SIZE, CELL_SIZE,
            )
            pygame.draw.rect(screen, color, rect)
