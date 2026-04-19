# Marker Tracker（标记物追踪）

> X 光序列（DICOM 多帧 / MP4 视频）中高密度标记物的自动检测、逐帧跟踪与距离测量工具。

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.10+ |
| 图像处理 | OpenCV |
| GUI | Tkinter |
| 数据格式 | DICOM (pydicom)、MP4/AVI |
| 数据分析 | NumPy、SciPy |
| 可视化 | Matplotlib |

## 功能特性

- **输入支持**：DICOM 多帧序列、MP4/AVI 视频统一接口
- **自动检测**：首帧自适应阈值 + 轮廓圆度筛选自动定位 Marker
- **手动选取**：CLI 指定坐标或 GUI 点选精确初始化
- **融合跟踪**：模板匹配 + Lucas-Kanade 光流双方法加权融合
- **质量门控**：失追段检测、帧间跳变告警、Marker ID 串换检测
- **指标计算**：Marker 间距离序列、运动位移/速度、Savitzky-Golay 平滑
- **Pixel Spacing 换算**：自动读取 DICOM Pixel Spacing，距离支持 mm 单位
- **报告导出**：CSV 距离表 + JSON 完整结果 + PNG 轨迹可视化 + Matplotlib 高质量曲线图
- **关键帧截图**：自动选取首帧/末帧/距离极值帧，叠加轨迹+距离标注

## 项目结构

```
marker-tracker/
├── src/
│   ├── __main__.py       # CLI 入口
│   ├── config.py         # 配置参数
│   ├── events.py         # 事件系统
│   ├── image_io.py       # 图像输入（DICOM/视频）
│   ├── init_marker.py    # Marker 初始化
│   ├── gui/              # Tkinter GUI
│   └── ...               # 跟踪/分析/导出模块
├── data/                 # 示例数据
├── samples/              # DICOM 样本文件
├── output/               # 输出结果
├── docs/
│   ├── PRD.md            # 产品需求文档
│   ├── TECHNICAL_DESIGN.md  # 技术方案
│   ├── TEST_CASES.md     # 测试用例
│   └── TASKS.md          # 任务追踪
├── pyproject.toml
├── requirements.txt
└── Makefile
```

## 使用

```bash
# 安装
pip install -e .

# CLI 模式
python -m marker_tracker --input sample.dcm --output result/

# GUI 模式
python -m marker_tracker --gui
```

## 相关笔记

- [心脏造影序列双 Marker 跟踪方案](/notes/marker-tracking) — 详细的技术方案与设计思路
