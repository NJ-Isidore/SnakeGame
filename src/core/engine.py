"""游戏引擎：主循环、场景管理、帧率控制"""
import time
import pygame
from src.core.state import (
    GameState, GameAction, FPS,
    WINDOW_WIDTH, WINDOW_HEIGHT,
)
from src.core.config import GameConfig
from src.core.input_handler import InputHandler


class GameEngine:
    """游戏引擎：管理游戏生命周期、场景切换和主循环"""

    def __init__(self, config: GameConfig | None = None):
        self.config = config or GameConfig()
        self.input = InputHandler(self.config.controls)
        self.running: bool = False
        self._state: GameState = GameState.MENU
        self._scene = None  # 当前场景对象
        self._prev_scene = None  # 暂存前一场景（用于暂停恢复）
        self._screen: pygame.Surface | None = None
        self._clock: pygame.time.Clock | None = None

    @property
    def state(self) -> GameState:
        """返回当前游戏状态"""
        return self._state

    @property
    def current_scene(self):
        """返回当前场景对象"""
        return self._scene

    def change_state(self, new_state: GameState) -> None:
        """改变游戏状态（不切换场景）"""
        self._state = new_state

    def init_display(self) -> None:
        """初始化 Pygame 显示"""
        pygame.init()
        self._screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        pygame.display.set_caption("贪吃蛇")
        self._clock = pygame.time.Clock()

    def run(self) -> None:
        """启动游戏主循环"""
        self.init_display()
        self.running = True
        self._setup_scene(GameState.MENU)

        while self.running:
            dt = self._clock.tick(FPS) / 1000.0
            self._handle_events()
            if self._scene:
                self._scene.update(dt)
                self._scene.render(self._screen)
            pygame.display.flip()

        pygame.quit()

    def _handle_events(self) -> None:
        """处理输入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                action = self.input.get_action(event.key)
                if action == GameAction.QUIT:
                    if self._state == GameState.MENU:
                        self.running = False
                    elif self._state == GameState.PLAYING:
                        if self._scene:
                            self._scene.handle_action(GameAction.PAUSE)
                    else:
                        self.switch_scene(GameState.MENU)
                elif self._scene:
                    self._scene.handle_action(action)

    def _setup_scene(self, state: GameState) -> None:
        """根据状态创建对应场景"""
        from src.ui.menu_scene import MenuScene
        from src.ui.play_scene import PlayScene
        from src.ui.pause_scene import PauseScene
        from src.ui.game_over_scene import GameOverScene
        from src.ui.settings_scene import SettingsScene
        from src.ui.leaderboard_scene import LeaderboardScene
        from src.ui.skin_select_scene import SkinSelectScene

        self._state = state
        scene_map = {
            GameState.MENU: lambda: MenuScene(self),
            GameState.PLAYING: lambda: PlayScene(self),
            GameState.PAUSED: lambda: PauseScene(self),
            GameState.GAME_OVER: lambda: GameOverScene(self),
            GameState.SETTINGS: lambda: SettingsScene(self),
            GameState.LEADERBOARD: lambda: LeaderboardScene(self),
            GameState.SKIN_SELECT: lambda: SkinSelectScene(self),
        }
        factory = scene_map.get(state)
        if factory:
            self._scene = factory()

    def switch_scene(self, state: GameState) -> None:
        """切换到指定场景"""
        if state == GameState.PAUSED:
            self._prev_scene = self._scene
        self._setup_scene(state)

    def restore_scene(self) -> None:
        """恢复到暂存的场景（如从暂停返回）"""
        if self._prev_scene is not None:
            self._state = GameState.PLAYING
            self._scene = self._prev_scene
            self._prev_scene = None
        else:
            self.switch_scene(GameState.PLAYING)
