"""排行榜场景"""
import pygame
from src.core.state import GameAction, GameState, WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.base_scene import BaseScene
from src.systems.scoring import ScoringSystem


class LeaderboardScene(BaseScene):
    """排行榜场景：展示历史最高分记录"""

    def __init__(self, engine):
        super().__init__(engine)
        scoring = ScoringSystem()
        self._entries = scoring.get_leaderboard()

    def handle_action(self, action: GameAction | None) -> None:
        """处理排行榜返回操作"""
        if action in (GameAction.CANCEL, GameAction.QUIT):
            self.engine.switch_scene(GameState.MENU)

    def update(self, dt: float) -> None:
        """更新排行榜状态（当前无需更新）"""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """渲染排行榜界面"""
        screen.fill((40, 40, 40))
        # 绘制标题
        self._draw_text(
            screen, "排行榜",
            WINDOW_WIDTH // 2, 60, font_size=40,
            color=(255, 215, 0),
        )
        if not self._entries:
            # 无记录时显示提示
            self._draw_text(
                screen, "暂无记录",
                WINDOW_WIDTH // 2, 200, font_size=24,
                color=(150, 150, 150),
            )
        else:
            # 绘制排行榜条目
            for i, entry in enumerate(self._entries[:10]):
                y = 120 + i * 35
                rank_color = (
                    (255, 215, 0) if i < 3 else (200, 200, 200)
                )
                text = f"#{i+1}  {entry.name}  {entry.score}  {entry.date}"
                self._draw_text(
                    screen, text,
                    WINDOW_WIDTH // 2, y, font_size=20,
                    color=rank_color,
                )
        # 绘制提示
        self._draw_text(
            screen, "ESC 返回",
            WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40,
            font_size=18, color=(120, 120, 120),
        )
