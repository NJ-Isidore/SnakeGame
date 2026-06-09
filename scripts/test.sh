#!/bin/bash
# 运行全部测试
set -e
cd "$(dirname "$0")/.."
uv run pytest tests/ -v --tb=short
