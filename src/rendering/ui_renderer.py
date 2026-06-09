"""UI 面板渲染器：右侧信息面板"""
import pygame
from src.core.state import (
    GAME_WIDTH, UI_PANEL_WIDTH, WINDOW_HEIGHT,
)


class UIRenderer:
    """UI 面板渲染器：绘制右侧信息面板"""

    def __init__(self, skin_manager):
        self._skin_mgr = skin_manager

    def draw_panel(
        self,
        screen: pygame.Surface,
        skin_id: str,
        score: int,
        high_score: int,
        level: int,
        lives: int,
        combo: int,
        speed: int,
    ) -> None:
        """绘制信息面板"""
        bg = self._skin_mgr.get_color(skin_id, "ui_bg")
        text_color = self._skin_mgr.get_color(skin_id, "ui_text")
        highlight = self._skin_mgr.get_color(skin_id, "ui_highlight")

        # 绘制面板背景
        panel_rect = pygame.Rect(
            GAME_WIDTH, 0, UI_PANEL_WIDTH, WINDOW_HEIGHT
        )
        pygame.draw.rect(screen, bg, panel_rect)
        pygame.draw.line(
            screen, text_color,
            (GAME_WIDTH, 0), (GAME_WIDTH, WINDOW_HEIGHT), 2,
        )

        # 绘制信息项
        x = GAME_WIDTH + 20
        y = 30
        font = pygame.font.SysFont("simsun", 20)

        items = [
            ("分数", str(score), highlight),
            ("最高分", str(high_score), text_color),
            ("等级", str(level), text_color),
            ("生命", "♥" * lives, (255, 80, 80)),
            ("连击", f"x{combo}" if combo > 0 else "-", text_color),
            ("速度", str(speed), text_color),
        ]
        for label, value, color in items:
            label_surf = font.render(f"{label}:", True, text_color)
            value_surf = font.render(value, True, color)
            screen.blit(label_surf, (x, y))
            screen.blit(value_surf, (x, y + 25))
            y += 65
