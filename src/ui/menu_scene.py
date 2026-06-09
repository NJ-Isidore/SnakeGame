"""主菜单场景"""
import pygame
from src.core.state import GameAction, GameState, WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.base_scene import BaseScene


class MenuScene(BaseScene):
    """主菜单场景：提供游戏入口和设置选项"""

    MENU_ITEMS = [
        ("开始游戏", GameState.PLAYING),
        ("设置", GameState.SETTINGS),
        ("排行榜", GameState.LEADERBOARD),
        ("皮肤", GameState.SKIN_SELECT),
        ("退出", None),
    ]

    def __init__(self, engine):
        super().__init__(engine)
        self._selected: int = 0

    def handle_action(self, action: GameAction | None) -> None:
        """处理菜单导航和选择"""
        if action is None:
            return
        if action == GameAction.MOVE_UP:
            self._selected = (self._selected - 1) % len(self.MENU_ITEMS)
        elif action == GameAction.MOVE_DOWN:
            self._selected = (self._selected + 1) % len(self.MENU_ITEMS)
        elif action == GameAction.CONFIRM or action == GameAction.MOVE_RIGHT:
            self._activate_selected()

    def _activate_selected(self) -> None:
        """激活选中的菜单项"""
        _, target = self.MENU_ITEMS[self._selected]
        if target is None:
            self.engine.running = False
        else:
            self.engine.switch_scene(target)

    def update(self, dt: float) -> None:
        """更新菜单状态（当前无需更新）"""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """渲染主菜单"""
        screen.fill((40, 40, 40))
        # 绘制标题
        self._draw_text(
            screen, "贪吃蛇",
            WINDOW_WIDTH // 2, 80, font_size=48,
        )
        # 绘制菜单项
        y_start = 180
        for i, (label, _) in enumerate(self.MENU_ITEMS):
            color = (0, 255, 0) if i == self._selected else (200, 200, 200)
            prefix = "> " if i == self._selected else "  "
            self._draw_text(
                screen, f"{prefix}{label}",
                WINDOW_WIDTH // 2, y_start + i * 50,
                font_size=28, color=color,
            )
        # 绘制提示
        self._draw_text(
            screen, "方向键选择，回车/右键确认",
            WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40,
            font_size=18, color=(120, 120, 120),
        )
