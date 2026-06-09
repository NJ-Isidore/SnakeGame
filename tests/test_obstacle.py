"""测试障碍物系统"""
from src.entities.obstacle import ObstacleManager


def test_initial_no_obstacles():
    """测试初始状态无障碍物"""
    mgr = ObstacleManager(grid_cols=20, grid_rows=20)
    assert mgr.count == 0
    assert mgr.all_positions == set()


def test_generate_obstacles():
    """测试生成障碍物"""
    mgr = ObstacleManager(grid_cols=20, grid_rows=20)
    occupied = {(10, 10), (9, 10), (8, 10), (5, 5)}
    mgr.generate(count=3, occupied=occupied)
    assert mgr.count == 3
    for pos in mgr.all_positions:
        assert pos not in occupied


def test_obstacles_dont_overlap():
    """测试障碍物不重叠"""
    mgr = ObstacleManager(grid_cols=20, grid_rows=20)
    occupied: set[tuple[int, int]] = set()
    mgr.generate(count=5, occupied=occupied)
    positions = mgr.all_positions
    assert len(positions) == 5


def test_clear_obstacles():
    """测试清除障碍物"""
    mgr = ObstacleManager(grid_cols=20, grid_rows=20)
    mgr.generate(count=3, occupied=set())
    mgr.clear()
    assert mgr.count == 0
