"""游戏场景：核心游戏玩法"""
import time
import pygame
from src.core.state import (
    Direction, GameAction, GameState, FoodType,
    GAME_WIDTH, GAME_HEIGHT, WINDOW_WIDTH,
    INITIAL_LIVES,
)
from src.ui.base_scene import BaseScene
from src.entities.snake import Snake
from src.entities.food import FoodFactory
from src.entities.obstacle import ObstacleManager
from src.systems.collision import CollisionDetector
from src.systems.scoring import ScoringSystem
from src.systems.difficulty import DifficultyManager
from src.rendering.renderer import Renderer
from src.rendering.ui_renderer import UIRenderer
from src.skins.skin_manager import SkinManager

# 动作到方向的映射表
DIR_ACTION_MAP = {
    GameAction.MOVE_UP: Direction.UP,
    GameAction.MOVE_DOWN: Direction.DOWN,
    GameAction.MOVE_LEFT: Direction.LEFT,
    GameAction.MOVE_RIGHT: Direction.RIGHT,
}


class PlayScene(BaseScene):
    """游戏场景：实现核心游戏玩法"""

    def __init__(self, engine):
        super().__init__(engine)
        config = engine.config
        skin_id = config.current_skin

        # 初始化子系统
        self._skin_mgr = SkinManager()
        self._renderer = Renderer(self._skin_mgr)
        self._ui_renderer = UIRenderer(self._skin_mgr)
        self._collision = CollisionDetector(
            config.grid_cols, config.grid_rows
        )
        self._scoring = ScoringSystem()
        self._difficulty = DifficultyManager()

        # 初始化游戏对象
        self._snake = Snake(
            start_pos=(config.grid_cols // 2, config.grid_rows // 2)
        )
        self._food_factory = FoodFactory(
            config.grid_cols, config.grid_rows
        )
        self._obstacles = ObstacleManager(
            config.grid_cols, config.grid_rows
        )

        # 游戏状态
        self._lives = config.initial_lives
        self._invincible_until: float = 0.0
        self._move_timer: float = 0.0
        self._game_time: float = 0.0
        self._skin_id = skin_id

        # 生成初始食物和加载最高分
        self._food = self._spawn_food()
        self._high_score = self._load_high_score()

    def _spawn_food(self):
        """生成新食物"""
        occupied = {seg.pos for seg in self._snake.segments}
        occupied.update(self._obstacles.all_positions)
        return self._food_factory.spawn(occupied)

    def _load_high_score(self) -> int:
        """加载历史最高分"""
        entries = self._scoring.get_leaderboard()
        return entries[0].score if entries else 0

    def handle_action(self, action: GameAction | None) -> None:
        """处理玩家输入"""
        if action is None:
            return
        if action in DIR_ACTION_MAP:
            self._snake.set_direction(DIR_ACTION_MAP[action])
        elif action == GameAction.PAUSE:
            self.engine.switch_scene(GameState.PAUSED)

    def update(self, dt: float) -> None:
        """更新游戏状态"""
        self._game_time += dt
        self._move_timer += dt
        self._difficulty.update_effects(self._game_time)

        # 根据当前速度决定是否移动
        move_interval = 1.0 / self._difficulty.speed
        if self._move_timer >= move_interval:
            self._move_timer -= move_interval
            self._tick()

    def _tick(self) -> None:
        """单次游戏逻辑更新"""
        self._snake.move()

        # 碰撞检测：墙壁
        if self._collision.hits_wall(self._snake):
            self._on_damage()
            return

        # 碰撞检测：障碍物
        if self._collision.hits_obstacle(self._snake, self._obstacles):
            self._on_damage()
            return

        # 碰撞检测：自身
        if self._collision.hits_self(self._snake):
            self._on_damage()
            return

        # 碰撞检测：食物
        if self._collision.hits_food(self._snake, self._food):
            food = self._food
            points = self._scoring.add_score(food.score)
            self._snake.grow(food.growth)

            # 减速食物效果
            if food.food_type == FoodType.SLOW:
                self._difficulty.apply_slow(5.0, self._game_time)

            # 检查升级和添加障碍物
            self._difficulty.check_level_up(self._scoring.score)
            self._maybe_add_obstacles()
            self._food = self._spawn_food()

        # 食物过期检查
        if self._food.is_expired(time.time()):
            self._food = self._spawn_food()

    def _on_damage(self) -> None:
        """处理伤害（扣血、重置蛇）"""
        if self._game_time < self._invincible_until:
            return
        self._lives -= 1
        self._scoring.reset_combo()
        if self._lives <= 0:
            self._scoring.save_to_leaderboard("Player")
            self.engine.switch_scene(GameState.GAME_OVER)
        else:
            # 重置蛇位置，短暂无敌
            config = self.engine.config
            self._snake = Snake(
                start_pos=(
                    config.grid_cols // 2,
                    config.grid_rows // 2,
                )
            )
            self._invincible_until = self._game_time + 2.0

    def _maybe_add_obstacles(self) -> None:
        """根据等级添加障碍物"""
        target = self._difficulty.obstacle_count_for_level(
            self._difficulty.level
        )
        current = self._obstacles.count
        if target > current:
            occupied = {seg.pos for seg in self._snake.segments}
            occupied.add(self._food.pos)
            self._obstacles.generate(target - current, occupied)

    def render(self, screen: pygame.Surface) -> None:
        """渲染游戏画面"""
        self._renderer.draw_background(screen, self._skin_id)
        self._renderer.draw_obstacles(screen, self._obstacles, self._skin_id)
        self._renderer.draw_food(screen, self._food, self._skin_id)
        self._renderer.draw_snake(screen, self._snake, self._skin_id)
        self._ui_renderer.draw_panel(
            screen, self._skin_id,
            score=self._scoring.score,
            high_score=self._high_score,
            level=self._difficulty.level,
            lives=self._lives,
            combo=self._scoring.combo,
            speed=self._difficulty.speed,
        )
