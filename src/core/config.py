"""游戏配置管理"""
import json
import os
from dataclasses import dataclass, field
from src.core.state import GRID_COLS, GRID_ROWS, CELL_SIZE

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config", "settings.json"
)

DEFAULT_CONTROLS: dict[str, str] = {
    "move_up": "UP",
    "move_down": "DOWN",
    "move_left": "LEFT",
    "move_right": "RIGHT",
    "pause": "SPACE",
    "quit": "ESCAPE",
}


@dataclass
class GameConfig:
    """游戏配置"""
    grid_cols: int = GRID_COLS
    grid_rows: int = GRID_ROWS
    cell_size: int = CELL_SIZE
    initial_speed: int = 8
    max_speed: int = 20
    initial_lives: int = 3
    current_skin: str = "classic"
    sound_enabled: bool = True
    sound_volume: float = 0.5
    controls: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_CONTROLS))
    _config_path: str = field(default=DEFAULT_CONFIG_PATH, repr=False)

    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self._config_path = config_path
        self.controls = dict(DEFAULT_CONTROLS)
        self.load()

    def save(self) -> None:
        """保存配置到文件"""
        data = {
            "current_skin": self.current_skin,
            "sound_enabled": self.sound_enabled,
            "sound_volume": self.sound_volume,
            "controls": self.controls,
        }
        os.makedirs(os.path.dirname(self._config_path), exist_ok=True)
        with open(self._config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        """从文件加载配置"""
        if not os.path.exists(self._config_path):
            return
        try:
            with open(self._config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.current_skin = data.get("current_skin", self.current_skin)
            self.sound_enabled = data.get("sound_enabled", self.sound_enabled)
            self.sound_volume = data.get("sound_volume", self.sound_volume)
            saved_controls = data.get("controls", {})
            self.controls.update(saved_controls)
        except (json.JSONDecodeError, OSError):
            pass
