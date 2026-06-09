"""暂停场景"""
import pygame
from src.core.state import GameAction, GameState, WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.base_scene import BaseScene


class PauseScene(BaseScene):
    """暂停场景：提供继续游戏或返回菜单的选项"""

    ITEMS = ["继续游戏", "返回主菜单"]

    def __init__(self, engine):
        super().__init__(engine)
        self._selected = 0

    def handle_action(self, action: GameAction | None) -> None:
        """处理暂停菜单导航"""
        if action is None:
            return
        if action == GameAction.MOVE_UP:
            self._selected = (self._selected - 1) % len(self.ITEMS)
        elif action == GameAction.MOVE_DOWN:
            self._selected = (self._selected + 1) % len(self.ITEMS)
        elif action in (GameAction.CONFIRM, GameAction.PAUSE):
            if self._selected == 0:
                self.engine.restore_scene()
            else:
                self.engine.switch_scene(GameState.MENU)

    def update(self, dt: float) -> None:
        """更新暂停状态（当前无需更新）"""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """渲染暂停覆盖层"""
        # 半透明黑色遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # 绘制标题
        self._draw_text(
            screen, "暂停",
            WINDOW_WIDTH // 2, 150, font_size=48,
        )
        # 绘制选项
        for i, label in enumerate(self.ITEMS):
            color = (0, 255, 0) if i == self._selected else (200, 200, 200)
            prefix = "> " if i == self._selected else "  "
            self._draw_text(
                screen, f"{prefix}{label}",
                WINDOW_WIDTH // 2, 250 + i * 50,
                font_size=28, color=color,
            )
