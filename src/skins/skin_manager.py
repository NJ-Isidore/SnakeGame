"""皮肤管理器"""
import json
import os

SKINS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config", "skins.json"
)


class SkinManager:
    """管理游戏皮肤的加载和查询"""

    def __init__(self, skins_path: str = SKINS_PATH):
        self._skins: dict[str, dict] = {}
        self._load(skins_path)

    def _load(self, path: str) -> None:
        """从 JSON 文件加载皮肤定义"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._skins = data.get("skins", {})

    def list_skin_ids(self) -> list[str]:
        """返回所有皮肤 ID 列表"""
        return list(self._skins.keys())

    def get_skin(self, skin_id: str) -> dict:
        """获取指定皮肤的定义，不存在时返回经典皮肤"""
        if skin_id not in self._skins:
            skin_id = "classic"
        return dict(self._skins.get(skin_id, {}))

    def get_color(self, skin_id: str, key: str) -> tuple[int, int, int]:
        """获取指定皮肤的某个颜色值"""
        skin = self.get_skin(skin_id)
        color = skin.get(key, [255, 255, 255])
        return tuple(color)
