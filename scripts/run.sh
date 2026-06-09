#!/bin/bash
# 启动贪吃蛇游戏
set -e
cd "$(dirname "$0")/.."
mkdir -p logs
uv run python main.py
