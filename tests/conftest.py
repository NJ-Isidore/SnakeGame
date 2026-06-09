"""pytest 公共 fixtures"""
import pytest


@pytest.fixture
def grid_size():
    """返回网格尺寸 (cols, rows)"""
    return (20, 20)


@pytest.fixture
def center_pos():
    """返回网格中心坐标"""
    return (10, 10)
