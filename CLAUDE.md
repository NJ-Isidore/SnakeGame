# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 常用命令

```bash
# 运行游戏
bash scripts/run.sh

# 运行全部测试（禁止直接调用 pytest）
bash scripts/test.sh

# 运行单个测试文件
uv run pytest tests/test_input_handler.py -v --tb=short

# 运行单个测试函数
uv run pytest tests/test_config.py::test_save_and_load_speed_preset -v

# 安装依赖
uv sync --extra dev
```

## 架构概览

### 场景驱动架构

游戏采用**场景模式**，由 `GameEngine`（`src/core/engine.py`）统一管理场景生命周期：

```
engine._handle_events() → InputHandler.get_action(key) → GameAction
                         → scene.handle_action(action)
                         → scene.update(dt)
                         → scene.render(screen)
```

所有场景继承 `BaseScene`（`src/ui/base_scene.py`），实现三个抽象方法：`handle_action`、`update`、`render`。

场景切换通过 `engine.switch_scene(GameState.XXX)` 触发，暂停时 `engine._prev_scene` 暂存前一场景，`engine.restore_scene()` 恢复。

### 依赖层级（单向，严禁反向）

```
core（state/config/input_handler/engine）
  ↓
entities（snake/food/obstacle）  ← 纯数据，无业务逻辑
  ↓
systems（collision/scoring/difficulty）  ← 游戏逻辑
  ↓
rendering（renderer/ui_renderer）  ← 纯绘制，不修改状态
  ↓
ui（各 scene）  ← 组合以上所有层
```

### 输入映射链路

`按键名(字符串)` → `KEY_NAME_MAP` → `pygame.K_*` → `_key_to_action` → `GameAction` → `scene.handle_action()`

默认按键映射定义在两处，必须保持一致：
- `src/core/input_handler.py` 的 `_build_mapping()` defaults
- `src/core/config.py` 的 `DEFAULT_CONTROLS`

### 速度系统

`SPEED_PRESETS`（`src/core/state.py`）定义用户可选的速度档位。`GameConfig.speed_preset` 存储当前选择，`PlayScene` 初始化时读取档位值传给 `DifficultyManager`。

## 编码规范

### 语言与注释
- 所有注释、docstring、commit message、错误信息**必须使用中文**
- 函数/方法必须有参数类型和返回值类型标注（type hints）

### 硬性约束
- 每个 Python 文件**不超过 300 行**，超过必须拆分
- 每层文件夹文件数**不超过 8 个**，超过需规划子文件夹
- 所有数值常量定义在 `src/core/state.py`，禁止业务代码中硬编码数字（magic number）

### TDD 流程
写测试 → 确认失败 → 写实现 → 确认通过 → 提交。每个模块独立验证，禁止全部写完再测试。

### 代码质量红线
- 禁止死代码（未使用的函数、变量、导入、注释掉的旧代码）
- 禁止重复代码（相同逻辑出现 2 次以上必须抽取）
- `try/except` 必须指定具体异常类型，禁止空 `except:`
- 对外部资源（文件读写、JSON 解析）必须有降级处理

### Git 提交格式
`feat:` / `fix:` / `refactor:` / `docs:` / `test:` + 中文描述。每个 Task 完成后独立提交。

## 技术栈

- **Python ≥ 3.12**，依赖管理仅使用 `uv`（禁止 pip/poetry/conda）
- **pygame-ce ≥ 2.5.0**（注意是 community edition，非 pygame）
- **hatchling** 构建后端，`src/` 布局
