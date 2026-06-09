"""游戏结束场景"""
import pygame
from src.core.state import GameAction, GameState, WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.base_scene import BaseScene


class GameOverScene(BaseScene):
    """游戏结束场景：提供重玩、查看排行榜或返回菜单的选项"""

    ITEMS = ["再来一局", "查看排行榜", "返回主菜单"]

    def __init__(self, engine):
        super().__init__(engine)
        self._selected = 0

    def handle_action(self, action: GameAction | None) -> None:
        """处理游戏结束菜单导航"""
        if action is None:
            return
        if action == GameAction.MOVE_UP:
            self._selected = (self._selected - 1) % len(self.ITEMS)
        elif action == GameAction.MOVE_DOWN:
            self._selected = (self._selected + 1) % len(self.ITEMS)
        elif action == GameAction.CONFIRM:
            if self._selected == 0:
                self.engine.switch_scene(GameState.PLAYING)
            elif self._selected == 1:
                self.engine.switch_scene(GameState.LEADERBOARD)
            else:
                self.engine.switch_scene(GameState.MENU)

    def update(self, dt: float) -> None:
        """更新游戏结束状态（当前无需更新）"""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """渲染游戏结束界面"""
        screen.fill((40, 40, 40))
        # 绘制标题
        self._draw_text(
            screen, "游戏结束",
            WINDOW_WIDTH // 2, 120, font_size=48,
            color=(255, 80, 80),
        )
        # 绘制选项
        for i, label in enumerate(self.ITEMS):
            color = (0, 255, 0) if i == self._selected else (200, 200, 200)
            prefix = "> " if i == self._selected else "  "
            self._draw_text(
                screen, f"{prefix}{label}",
                WINDOW_WIDTH // 2, 230 + i * 50,
                font_size=28, color=color,
            )
