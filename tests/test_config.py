"""测试配置系统"""
import json
import tempfile
import os
from src.core.config import GameConfig, DEFAULT_CONTROLS


def test_default_config_values():
    """测试默认配置值"""
    config = GameConfig()
    assert config.grid_cols == 20
    assert config.grid_rows == 20
    assert config.cell_size == 25
    assert config.initial_speed == 8
    assert config.max_speed == 20
    assert config.initial_lives == 3
    assert config.current_skin == "classic"
    assert config.sound_enabled is True


def test_controls_are_dict():
    """测试默认按键配置"""
    config = GameConfig()
    assert isinstance(config.controls, dict)
    assert "move_up" in config.controls
    assert "move_down" in config.controls


def test_save_and_load_config():
    """测试配置保存和加载"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        temp_path = f.name

    try:
        config = GameConfig(config_path=temp_path)
        config.current_skin = "neon"
        config.sound_enabled = False
        config.save()

        loaded = GameConfig(config_path=temp_path)
        assert loaded.current_skin == "neon"
        assert loaded.sound_enabled is False
    finally:
        os.unlink(temp_path)


def test_load_missing_file_uses_defaults():
    """测试加载不存在的文件时使用默认值"""
    config = GameConfig(config_path="/tmp/nonexistent_snake_config.json")
    assert config.current_skin == "classic"
    assert config.sound_enabled is True


def test_default_speed_preset():
    """测试默认速度档位为'普通'"""
    config = GameConfig()
    assert config.speed_preset == "普通"


def test_save_and_load_speed_preset():
    """测试速度档位保存和加载"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        temp_path = f.name

    try:
        config = GameConfig(config_path=temp_path)
        config.speed_preset = "慢速"
        config.save()

        loaded = GameConfig(config_path=temp_path)
        assert loaded.speed_preset == "慢速"
    finally:
        os.unlink(temp_path)


def test_default_controls_include_confirm():
    """测试默认按键配置包含 CONFIRM"""
    config = GameConfig()
    assert "confirm" in config.controls
    assert config.controls["confirm"] == "ENTER"
