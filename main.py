"""贪吃蛇游戏入口"""
from src.core.config import GameConfig
from src.core.engine import GameEngine


def main():
    """启动游戏"""
    config = GameConfig()
    engine = GameEngine(config)
    engine.run()


if __name__ == "__main__":
    main()
