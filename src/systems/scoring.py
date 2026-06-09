"""计分系统：分数计算、连击倍率、排行榜持久化"""
import json
import os
from dataclasses import dataclass, asdict
from datetime import date

DEFAULT_LEADERBOARD_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config", "leaderboard.json"
)
MAX_LEADERBOARD = 10


@dataclass
class ScoreEntry:
    """排行榜条目"""
    name: str
    score: int
    date: str


class ScoringSystem:
    """计分系统：管理分数、连击和排行榜"""

    def __init__(self, leaderboard_path: str = DEFAULT_LEADERBOARD_PATH):
        self._score: int = 0
        self._combo: int = 0
        self._path = leaderboard_path

    @property
    def score(self) -> int:
        """返回当前分数"""
        return self._score

    @property
    def combo(self) -> int:
        """返回当前连击数"""
        return self._combo

    def add_score(self, base_points: int) -> int:
        """加分并返回实际得分（含连击倍率）"""
        self._combo += 1
        multiplier = max(1, self._combo)
        points = base_points * multiplier
        self._score += points
        return points

    def reset_combo(self) -> None:
        """重置连击"""
        self._combo = 0

    def reset(self) -> None:
        """重置分数和连击"""
        self._score = 0
        self._combo = 0

    def save_to_leaderboard(self, name: str) -> None:
        """保存当前分数到排行榜"""
        entries = self._load_entries()
        entry = ScoreEntry(
            name=name,
            score=self._score,
            date=date.today().isoformat(),
        )
        entries.append(asdict(entry))
        entries.sort(key=lambda e: e["score"], reverse=True)
        entries = entries[:MAX_LEADERBOARD]
        self._save_entries(entries)

    def get_leaderboard(self) -> list[ScoreEntry]:
        """获取排行榜"""
        raw = self._load_entries()
        return [ScoreEntry(**e) for e in raw]

    def _load_entries(self) -> list[dict]:
        """从文件加载排行榜数据"""
        if not os.path.exists(self._path):
            return []
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    def _save_entries(self, entries: list[dict]) -> None:
        """保存排行榜数据到文件"""
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
