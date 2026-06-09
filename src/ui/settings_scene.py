"""设置场景：音效开关、速度调节、按键重映射"""
import pygame
from src.core.state import (
    GameAction, GameState, WINDOW_WIDTH, WINDOW_HEIGHT,
    SPEED_PRESET_NAMES,
)
from src.ui.base_scene import BaseScene


class SettingsScene(BaseScene):
    """设置场景：提供音效开关、速度调节和按键重映射功能"""

    def __init__(self, engine):
        super().__init__(engine)
        self._selected = 0
        config = engine.config
        self._speed_names = SPEED_PRESET_NAMES
        self._rebinding: bool = False
        self._rebind_action: str = ""
        self._action_names = list(config.controls.keys())
        self._items = self._build_items()

    def _build_items(self) -> list[str]:
        """根据当前配置构建菜单项列表"""
        config = self.engine.config
        sound_state = "开启" if config.sound_enabled else "关闭"
        return [
            f"音效: {sound_state}",
            f"速度: {config.speed_preset}",
            "按键设置",
            "保存并返回",
        ]

    def _toggle_sound(self) -> None:
        """切换音效开关"""
        self.engine.config.sound_enabled = (
            not self.engine.config.sound_enabled
        )
        state = "开启" if self.engine.config.sound_enabled else "关闭"
        self._items[0] = f"音效: {state}"

    def _cycle_speed(self, forward: bool) -> None:
        """切换速度档位（向前/向后循环）"""
        names = self._speed_names
        current = self.engine.config.speed_preset
        idx = names.index(current) if current in names else 0
        idx = (idx + (1 if forward else -1)) % len(names)
        self.engine.config.speed_preset = names[idx]
        self._items[1] = f"速度: {names[idx]}"

    def handle_action(self, action: GameAction | None) -> None:
        """处理设置菜单导航和交互"""
        if action is None:
            return
        if self._rebinding:
            self._handle_rebind(action)
            return
        if action == GameAction.MOVE_UP:
            self._selected = (self._selected - 1) % len(self._items)
        elif action == GameAction.MOVE_DOWN:
            self._selected = (self._selected + 1) % len(self._items)
        elif action in (GameAction.MOVE_LEFT, GameAction.MOVE_RIGHT):
            # 左右方向键切换速度档位
            if self._selected == 1:
                self._cycle_speed(action == GameAction.MOVE_RIGHT)
        elif action == GameAction.CONFIRM:
            if self._selected == 0:
                self._toggle_sound()
            elif self._selected == 2:
                self._rebinding = True
            elif self._selected == 3:
                self.engine.config.save()
                self.engine.input.update_controls(
                    self.engine.config.controls
                )
                self.engine.switch_scene(GameState.MENU)
        elif action == GameAction.CANCEL:
            self.engine.switch_scene(GameState.MENU)

    def _handle_rebind(self, action: GameAction | None) -> None:
        """处理按键重绑定"""
        # 简化版：按任意方向键完成重绑定
        key_map = {
            GameAction.MOVE_UP: "UP",
            GameAction.MOVE_DOWN: "DOWN",
            GameAction.MOVE_LEFT: "LEFT",
            GameAction.MOVE_RIGHT: "RIGHT",
        }
        if action in key_map:
            self._rebinding = False

    def update(self, dt: float) -> None:
        """更新设置状态（当前无需更新）"""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """渲染设置界面"""
        screen.fill((40, 40, 40))
        title = "重绑定模式" if self._rebinding else "设置"
        self._draw_text(
            screen, title,
            WINDOW_WIDTH // 2, 80, font_size=40,
        )
        if self._rebinding:
            self._draw_text(
                screen, "按方向键设置...",
                WINDOW_WIDTH // 2, 200, font_size=24,
                color=(255, 255, 0),
            )
        else:
            for i, label in enumerate(self._items):
                color = (
                    (0, 255, 0) if i == self._selected
                    else (200, 200, 200)
                )
                prefix = "> " if i == self._selected else "  "
                self._draw_text(
                    screen, f"{prefix}{label}",
                    WINDOW_WIDTH // 2, 180 + i * 50,
                    font_size=28, color=color,
                )
            self._draw_text(
                screen, "← → 调节速度，回车确认，ESC 返回",
                WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40,
                font_size=18, color=(120, 120, 120),
            )
