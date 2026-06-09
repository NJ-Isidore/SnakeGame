"""输入处理：将键盘按键映射为游戏动作"""
import pygame
from src.core.state import GameAction

# 按键名 -> pygame 常量
KEY_NAME_MAP: dict[str, int] = {
    "UP": pygame.K_UP,
    "DOWN": pygame.K_DOWN,
    "LEFT": pygame.K_LEFT,
    "RIGHT": pygame.K_RIGHT,
    "SPACE": pygame.K_SPACE,
    "ESCAPE": pygame.K_ESCAPE,
    "ENTER": pygame.K_RETURN,
    "w": pygame.K_w,
    "a": pygame.K_a,
    "s": pygame.K_s,
    "d": pygame.K_d,
}

# 动作名 -> GameAction
ACTION_MAP: dict[str, GameAction] = {
    "move_up": GameAction.MOVE_UP,
    "move_down": GameAction.MOVE_DOWN,
    "move_left": GameAction.MOVE_LEFT,
    "move_right": GameAction.MOVE_RIGHT,
    "pause": GameAction.PAUSE,
    "quit": GameAction.QUIT,
    "confirm": GameAction.CONFIRM,
    "cancel": GameAction.CANCEL,
}


class InputHandler:
    """输入处理器：管理按键到游戏动作的映射"""

    def __init__(self, controls: dict[str, str] | None = None):
        self._key_to_action: dict[int, GameAction] = {}
        self._build_mapping(controls or {})

    def _build_mapping(self, controls: dict[str, str]) -> None:
        """构建按键到动作的映射表"""
        # 默认映射
        defaults = {
            "move_up": "UP", "move_down": "DOWN",
            "move_left": "LEFT", "move_right": "RIGHT",
            "pause": "SPACE", "quit": "ESCAPE",
        }
        merged = {**defaults, **controls}
        self._key_to_action.clear()
        for action_name, key_name in merged.items():
            key_code = KEY_NAME_MAP.get(key_name)
            action = ACTION_MAP.get(action_name)
            if key_code is not None and action is not None:
                self._key_to_action[key_code] = action

    def update_controls(self, controls: dict[str, str]) -> None:
        """更新按键配置"""
        self._build_mapping(controls)

    def get_action(self, key: int) -> GameAction | None:
        """获取按键对应的游戏动作"""
        return self._key_to_action.get(key)
