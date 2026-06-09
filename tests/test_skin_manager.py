"""测试皮肤管理器"""
from src.skins.skin_manager import SkinManager


def test_load_default_skin():
    """测试加载默认皮肤"""
    manager = SkinManager()
    skin = manager.get_skin("classic")
    assert skin["name"] == "经典"
    assert len(skin["snake_head"]) == 3


def test_list_skin_ids():
    """测试列出所有皮肤 ID"""
    manager = SkinManager()
    ids = manager.list_skin_ids()
    assert "classic" in ids
    assert "retro" in ids
    assert "neon" in ids


def test_unknown_skin_returns_classic():
    """测试未知皮肤返回经典皮肤"""
    manager = SkinManager()
    skin = manager.get_skin("nonexistent")
    classic = manager.get_skin("classic")
    assert skin == classic


def test_get_color():
    """测试获取颜色值"""
    manager = SkinManager()
    color = manager.get_color("classic", "snake_head")
    assert color == (0, 200, 0)
