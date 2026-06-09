"""场景基类：所有 UI 场景的公共接口"""
from abc import ABC, abstractmethod
import pygame
from src.core.state import GameAction


class BaseScene(ABC):
    """场景抽象基类：定义场景的公共接口"""

    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    def handle_action(self, action: GameAction | None) -> None:
        """处理用户输入动作"""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """更新场景状态"""
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """渲染场景"""
        pass

    def _draw_text(
        self,
        screen: pygame.Surface,
        text: str,
        x: int,
        y: int,
        font_size: int = 32,
        color: tuple = (255, 255, 255),
        center: bool = True,
    ) -> None:
        """绘制文本的辅助方法"""
        font = pygame.font.SysFont("simsun", font_size)
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        screen.blit(surface, rect)
