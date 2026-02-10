# AGENTS.md

科研论文解析 Agent (CrewAI + Markitdown)

## 项目概述

本项目旨在开发一个基于 CrewAI 框架的智能 Agent 系统，模拟科研人员的阅读习惯（略读、精读、批判性评估），从 PDF 论文中提取深度结构化信息。使用 OpenDataLab `Mineru` 库作为底层解析引擎，以获取包含多模态信息（如图片描述、表格）的 Markdown 文本。

## 技术栈

* **核心框架**: CrewAI (Agent 编排)
* **PDF 解析**: OpenDataLab Mineru (Magic-PDF，支持 PDF 转 Markdown，含图像 OCR 处理)
* **语言模型**: 建议使用 Claude 3.5 Sonnet 或 GPT-4o (具备极强的长文本和逻辑推理能力)
* **向量数据库**: ChromaDB (用于章节检索)

## 编程准则

* **模块化设计**: 解析模块、Agent 逻辑、任务逻辑需严格解耦。
* **解析优先**: 在启动任何任务前，必须调用 `Mineru` 生成完整的文本镜像。
* **语义分块**: 针对论文结构（Introduction, Method, Result, Conclusion）进行正则匹配或语义切分，避免简单的 Token 切割。
* **输出格式**: 所有 Agent 的中间输出应保持结构化（JSON 或 Markdown 列表）。

## Agent 角色定义

1. **略读专家 (Skimmer)**:
* **职责**: 快速阅读摘要、引言末尾和结论。
* **目标**: 提取论文的核心贡献、解决的问题及全文逻辑大纲。


2. **结构分析师 (Scanning Specialist)**:
* **职责**: 深入解析 `Mineru` 提取的图表描述和方法论章节。
* **目标**: 还原实验流程（如 PEMD 的四阶段逻辑），提取关键物理量和公式。


3. **评审专家 (Critical Reviewer)**:
* **职责**: 对比结果与目标，寻找逻辑漏洞或实验局限。
* **目标**: 提供批判性视角，总结论文的真实影响力和改进方向。



## 任务流设计 (Process Workflow)

1. **Task: Pre-processing**: 调用 `Mineru` 处理上传的 PDF，保存为 `temp_paper.md`。
2. **Task: Skimming**: Skimmer Agent 生成“研究摘要卡片”。
3. **Task: Deep Dive**: Scanning Specialist 根据摘要卡片，按章节提取算法、流程图逻辑。
4. **Task: Validation**: Critical Reviewer 检查结果章节是否支撑了摘要中的声明。

## 核心实现逻辑参考

```python
# 示例：Mineru 集成
import os
from pathlib import Path
from mineru.cli.common import read_fn
from mineru.backend.hybrid.hybrid_analyze import doc_analyze as hybrid_doc_analyze
from mineru.data.data_reader_writer import FileBasedDataWriter
from mineru.utils.engine_utils import get_vlm_engine

def parse_paper(file_path):
    # 配置 Mineru
    pdf_bytes = read_fn(file_path)
    output_dir = "output/temp"
    
    # 准备环境 (简化版)
    backend = "auto-engine" # 或 vlm-auto-engine
    # ... 调用核心解析逻辑 ...
    # 参考 demo.py 的实现
    
    return md_content

# 示例：CrewAI 任务分派
# 需定义包含特定逻辑的 Task(description=..., expected_output=..., agent=...)

```

## 目录结构建议

* `/src/agents/`: 存放各 Agent 的配置文件。
* `/src/tools/`: 存放 `Mineru` 解析工具类。
* `/src/tasks/`: 定义 CrewAI 的任务逻辑。
* `/output/`: 存放解析后的结构化报告。

## 编程规范

没问题！这是为您翻译好的中文版本，您可以直接将其更新到您的 `CLAUDE.md` 文件中。

---

### 1. 构建、检查 (Lint) 与测试命令

#### 依赖管理

* **安装依赖**: `uv sync`
* **添加依赖**: `uv add <package>`
* **添加开发依赖**: `uv add --dev <package>`

#### 代码检查与格式化

我们统一使用 `ruff` 进行代码检查和格式化。

* **格式化代码**: `uv run ruff format .`
* **检查代码（自动修复）**: `uv run ruff check --fix .`
* **类型检查**: `uv run mypy .` (请确保已安装 `mypy`: `uv add --dev mypy`)

#### 测试

我们使用 `pytest` 进行测试。

* **运行所有测试**: `uv run pytest`
* **运行单个测试文件**: `uv run pytest tests/test_file.py`
* **运行特定测试项目**: `uv run pytest tests/test_file.py::test_function_name`
* **运行并生成覆盖率报告**: `uv run pytest --cov=src`

---

### 2. 代码风格与规范

#### 通用 Python 准则

* 遵循 **PEP 8** 标准（通过 `ruff` 强制执行）。
* **类型提示 (Type Hints)**: 所有函数参数和返回值**必须**标注严格的类型提示。
```python
def process_data(data: dict[str, Any]) -> list[str]:
    ...

```

* **文档字符串 (Docstrings)**: 所有公开模块、类和函数均需使用 **Google 风格** 的文档字符串。
```python
def fetch_paper(url: str) -> Paper:
    """从指定的 URL 获取论文。

    Args:
        url: 论文的 URL 地址。

    Returns:
        包含内容的 Paper 对象。
    """

```

#### 导入规范

* 优先使用绝对导入而非相对导入。
* 导入分组顺序：标准库 -> 第三方库 -> 本地模块（通过 `ruff` 强制执行）。

#### 命名约定

* **变量/函数**: `snake_case` (蛇形命名法)
* **类**: `PascalCase` (大驼峰命名法)
* **常量**: `UPPER_CASE` (全大写)
* **私有成员**: `_leading_underscore` (前置下划线)

#### 错误处理

* 使用具体的异常类（自定义或内置），避免直接使用模糊的 `Exception`。
* `try/except` 块应尽可能紧凑地包裹可能抛出异常的代码。
* 使用标准 `logging` 模块或 `structlog` 记录错误，禁止使用 `print`。

#### 项目结构

* 随着项目增长，优先采用 `src/` 布局。
* 保持 `main.py` 作为一个轻量级的入口点。
* 测试代码存放在 `tests/` 目录中，其结构应与源代码目录镜像对应。

### 3. Agent 开发工作流

1. **验证**: 在完成任务前，务必运行 `uv run ruff check .` 和 `uv run pytest`。
2. **依赖**: 如果引入了新包，必须通过 `uv add` 添加。
3. **重构**: 重构时要确保现有测试全部通过，并针对边缘情况添加新测试。
4. **文件命名**: 除非绝对必要，否则不要使用 `utils.py` 等泛泛的名称；优先使用具体的模块名（例如 `text_processing.py`）。
5. **提交信息**: 使用清晰、描述性的提交信息，遵循约定式提交规范（Conventional Commits）。
