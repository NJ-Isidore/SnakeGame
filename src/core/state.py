"""游戏状态枚举与全局常量"""
from enum import Enum


class Direction(Enum):
    """蛇的移动方向"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def dx(self) -> int:
        """X 轴偏移量"""
        return self.value[0]

    @property
    def dy(self) -> int:
        """Y 轴偏移量"""
        return self.value[1]

    @property
    def opposite(self) -> "Direction":
        """返回相反方向"""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites[self]


class GameState(Enum):
    """游戏状态"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"
    LEADERBOARD = "leaderboard"
    SKIN_SELECT = "skin_select"


class FoodType(Enum):
    """食物类型"""
    NORMAL = "normal"      # +10 分
    BONUS = "bonus"        # +30 分，限时出现
    SLOW = "slow"          # +10 分，临时减速
    GROWTH = "growth"      # +20 分，额外增长


class GameAction(Enum):
    """游戏动作（由输入映射而来）"""
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    PAUSE = "pause"
    QUIT = "quit"
    CONFIRM = "confirm"
    CANCEL = "cancel"


# ===== 网格与显示常量 =====
GRID_COLS = 20
GRID_ROWS = 20
CELL_SIZE = 25
GAME_WIDTH = GRID_COLS * CELL_SIZE        # 500px
GAME_HEIGHT = GRID_ROWS * CELL_SIZE       # 500px
UI_PANEL_WIDTH = 200
WINDOW_WIDTH = GAME_WIDTH + UI_PANEL_WIDTH  # 700px
WINDOW_HEIGHT = GAME_HEIGHT               # 500px
FPS = 60

# ===== 游戏参数常量 =====
INITIAL_SPEED = 8         # 初始速度（步/秒）
MAX_SPEED = 20            # 最大速度
INITIAL_LIVES = 3         # 初始生命数
SPEED_INCREMENT = 1       # 每级速度增量
SCORE_PER_LEVEL = 50      # 每多少分升级
