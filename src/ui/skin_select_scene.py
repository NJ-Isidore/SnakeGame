"""皮肤选择场景"""
import pygame
from src.core.state import GameAction, GameState, WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.base_scene import BaseScene
from src.skins.skin_manager import SkinManager


class SkinSelectScene(BaseScene):
    """皮肤选择场景：提供皮肤切换和预览功能"""

    def __init__(self, engine):
        super().__init__(engine)
        self._skin_mgr = SkinManager()
        self._skin_ids = self._skin_mgr.list_skin_ids()
        # 定位到当前选中的皮肤
        current = engine.config.current_skin
        if current in self._skin_ids:
            self._selected = self._skin_ids.index(current)
        else:
            self._selected = 0

    def handle_action(self, action: GameAction | None) -> None:
        """处理皮肤选择导航和确认"""
        if action is None:
            return
        if action == GameAction.MOVE_UP:
            self._selected = (
                (self._selected - 1) % len(self._skin_ids)
            )
        elif action == GameAction.MOVE_DOWN:
            self._selected = (
                (self._selected + 1) % len(self._skin_ids)
            )
        elif action == GameAction.CONFIRM:
            skin_id = self._skin_ids[self._selected]
            self.engine.config.current_skin = skin_id
            self.engine.config.save()
            self.engine.switch_scene(GameState.MENU)
        elif action == GameAction.CANCEL:
            self.engine.switch_scene(GameState.MENU)

    def update(self, dt: float) -> None:
        """更新皮肤选择状态（当前无需更新）"""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """渲染皮肤选择界面"""
        screen.fill((40, 40, 40))
        # 绘制标题
        self._draw_text(
            screen, "选择皮肤",
            WINDOW_WIDTH // 2, 80, font_size=40,
        )
        # 绘制皮肤列表
        for i, skin_id in enumerate(self._skin_ids):
            skin = self._skin_mgr.get_skin(skin_id)
            name = skin.get("name", skin_id)
            is_current = (
                skin_id == self.engine.config.current_skin
            )
            is_selected = (i == self._selected)

            # 根据状态设置颜色和前缀
            if is_selected:
                color = (0, 255, 0)
                prefix = "> "
            elif is_current:
                color = (255, 215, 0)
                prefix = "* "
            else:
                color = (200, 200, 200)
                prefix = "  "

            suffix = " (当前)" if is_current else ""
            self._draw_text(
                screen, f"{prefix}{name}{suffix}",
                WINDOW_WIDTH // 2, 180 + i * 50,
                font_size=28, color=color,
            )

        # 绘制颜色预览
        if self._skin_ids:
            skin = self._skin_mgr.get_skin(
                self._skin_ids[self._selected]
            )
            preview_y = 350
            keys = ["snake_head", "snake_body", "food_normal"]
            for j, key in enumerate(keys):
                c = tuple(skin.get(key, [255, 255, 255]))
                rect = pygame.Rect(
                    WINDOW_WIDTH // 2 - 60 + j * 50,
                    preview_y, 40, 40,
                )
                pygame.draw.rect(screen, c, rect, border_radius=6)

        # 绘制提示
        self._draw_text(
            screen, "方向键选择，回车确认，ESC 返回",
            WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40,
            font_size=18, color=(120, 120, 120),
        )
