"""测试输入处理"""
from src.core.input_handler import InputHandler
from src.core.state import GameAction


def test_map_key_to_action():
    """测试默认按键映射"""
    handler = InputHandler()
    # 默认映射：上方向键 -> MOVE_UP
    import pygame
    action = handler.get_action(pygame.K_UP)
    assert action == GameAction.MOVE_UP


def test_custom_controls():
    """测试自定义按键配置"""
    handler = InputHandler()
    handler.update_controls({"move_up": "w", "move_down": "s"})
    import pygame
    assert handler.get_action(pygame.K_w) == GameAction.MOVE_UP
    assert handler.get_action(pygame.K_s) == GameAction.MOVE_DOWN


def test_unknown_key_returns_none():
    """测试未知按键返回 None"""
    handler = InputHandler()
    action = handler.get_action(99999)
    assert action is None


def test_confirm_key_mapping():
    """测试回车键映射为 CONFIRM 动作"""
    import pygame
    handler = InputHandler()
    assert handler.get_action(pygame.K_RETURN) == GameAction.CONFIRM


def test_confirm_in_custom_controls():
    """测试自定义配置中 CONFIRM 映射可覆盖"""
    import pygame
    handler = InputHandler({"confirm": "SPACE"})
    assert handler.get_action(pygame.K_SPACE) == GameAction.CONFIRM
