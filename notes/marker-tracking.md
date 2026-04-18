---
title: 心脏造影序列双 marker 跟踪与距离变化曲线方案
date: 2026-04-08
tags: [医学影像, 造影序列, DICOM, OpenCV, 时序跟踪]
category: medical-imaging
---


> **主题**：医学影像 / 心脏造影 / DICOM / marker 跟踪 / 距离曲线
> **日期**：2026 年 4 月 8 日
> **标签**：医学影像 / 造影序列 / DICOM / OpenCV / 时序跟踪

---

**如果把医生的真实需求翻成技术问题，这题已经不是“静态黑点间距识别”，而是“在心脏造影序列中逐帧定位两个 marker，并输出从开头到结尾的距离变化曲线”。真正靠谱的路线，不是直接追某个单点检测算法，而是把序列解码、首帧初始化、逐帧跟踪、失追恢复、时间轴构建和距离曲线输出串成一条稳定链路。**

> **封面**：covers/断线黑点间距识别方案_cover.png

这类需求乍看像一个简单的点检测问题，实际更接近一个小型医学影像测量系统。只要把目标从“识别两个黑点”升级成“输出可信的时序距离结果”，方案设计就得同时考虑成像质量、逐帧运动、marker 失追、时间轴定义和物理量换算。

可以把它想象成在一段不断晃动的心脏造影视频里，手里始终盯着两个会跟着心跳和呼吸一起动的点。医生真正想看的，不是某一帧里这两个点离得多远，而是**整段影像中它们的距离如何随时间变化**。一旦把问题这么定义，算法重点就从“找点”变成了“持续、稳定、可解释地跟踪这两个点”。

医生这次补充的信息其实很关键：输入优先是 **DICOM 造影文件**，但 `mp4` 也可能出现；序列里存在明显的**心脏搏动和呼吸运动**；目标不是一串点，也不是一条曲线，而是**固定的两个 marker**；交付物不是单个距离值，而是一条从影像开头到结尾的 `d(t)` 曲线。这个任务更接近“序列中的双目标跟踪 + 医学测量导出”，而不是前一版文档里偏静态的几何分析题。

## 一页版简述：非专业读者先看

如果只用一句话概括，这件事是：给一段心脏造影序列，先在首帧确定两个 marker 的位置，再让程序逐帧跟着它们走，最后把两点之间的距离随时间画成一条曲线。

对非专业读者，最重要的是下面 5 件事：

- **这件事能不能做**
  - 能做，而且第一版不必先上大模型。
- **第一版最实际的做法**
  - 首帧人工点两下两个 marker，后面用局部跟踪自动往后跑。
- **为什么 DICOM 更值钱**
  - DICOM 更容易保留像素数据和多帧时间信息；如果还能拿到 `Pixel Spacing`，距离结果就有机会从像素升级到毫米 [[15]](https://pydicom.github.io/pydicom/stable/guides/user/working_with_pixel_data.html) [[18]](https://dicom.innolitics.com/ciods/ultrasound-multi-frame-image/cine/00181065) [[14]](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_10.7.html)。
- **真正要交付什么**
  - 不是某一帧截图，而是一条 `d(frame)` 或 `d(t)` 曲线，并标出低置信度帧。
- **有没有现成开源工具可以直接拿来用**
  - 有现成开源工具，但大多只能拿来做原型、标注或对照，不是开箱即用的“心脏造影双 marker 成品”。

如果今天就要给医生看第一版结果，最稳的路线仍然是：`DICOM 优先 -> 首帧人工初始化 -> 模板匹配 / 光流 -> 输出原始距离曲线 -> 再补时间轴和毫米换算`。

## 有没有现成的开源方案：有，但大多不能直接交付

如果问题只是“有没有开源工具能试”，答案是有；如果问题是“有没有一个开箱即用、专门针对心脏造影双 marker、能直接生成临床可解释距离曲线的成品”，我当前更倾向于回答**没有现成成熟方案可以直接替代定制实现**。从主流开源工具看，它们大多分成两类：一类是通用 tracking 平台，一类是医学影像浏览 / 标注平台。

| 方案 | 能不能用 | 更适合的阶段 | 为什么 |
|------|------|------|------|
| Fiji / TrackMate | **可以试** | 快速原型、半人工基线 | TrackMate 自带界面，支持 tracking、结果编辑和轨迹分析，也允许手动修正结果 [[19]](https://imagej.net/plugins/trackmate/)。但它主要面向 microscopy 的 spot / cell tracking，典型 spot 场景更接近亮点配暗背景；对造影里的黑色 marker，通常还要先做反相或自定义预处理。它更像原型工具，不是现成的 DICOM 双 marker 交付方案。 |
| 3D Slicer + Sequences | **可以辅助用** | DICOM 浏览、回放、人工校验、标注 | 3D Slicer 的 Sequences 模块可以创建和可视化时序节点，也支持把 DICOM 作为 Sequence node 加载 [[20]](https://slicer.readthedocs.io/en/latest/user_guide/modules/sequences.html)。这很适合看片、回放和人工校对，但它本身不是现成的双 marker tracker。 |
| Ultralytics YOLO Track | **后续可用** | 有标注数据后的检测 + 跟踪 | Ultralytics 提供 `track` 模式，支持 BoT-SORT、ByteTrack 和自定义 tracker 配置，也支持配合自训练模型工作 [[21]](https://docs.ultralytics.com/modes/track/)。如果后面能积累稳定标注数据，它有机会成为更自动化的路线；但对“只有两个 marker、先要出第一条曲线”的任务来说，第一版通常太重。 |
| MMTracking | **更偏研究平台** | 模型研究、复杂场景升级 | MMTracking 是 OpenMMLab 的视频感知工具箱，支持 `SOT`、`MOT`、`VID`、`VIS`，模块化很强 [[22]](https://mmtracking.readthedocs.io/en/dev-1.x/overview.html)。但它更像研究框架，不像能直接套在当前医学场景上的现成产品。 |

对当前这道题，我更建议把这些开源工具这样分工：

- **TrackMate / 3D Slicer**
  - 适合拿来做快速对照、人工校验、原型验证。
- **YOLO Track / MMTracking**
  - 适合在后续数据积累起来之后，评估要不要从“传统视觉 + 半人工”升级到“检测 + 跟踪”。
- **pydicom + OpenCV 自己搭的小链路**
  - 反而最适合当前阶段。因为它最容易把 `DICOM` 读取、`Frame Time Vector`、`Pixel Spacing`、A/B 编号和低置信度帧规则放在同一套逻辑里 [[15]](https://pydicom.github.io/pydicom/stable/guides/user/working_with_pixel_data.html) [[16]](https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html) [[17]](https://docs.opencv.org/4.x/db/d7f/tutorial_js_lucas_kanade.html) [[18]](https://dicom.innolitics.com/ciods/ultrasound-multi-frame-image/cine/00181065)。

如果目标是**一两周内给医生看能讨论的 PoC**，我不建议第一步就直接压在 `YOLO` / `MMTracking` 上；如果目标是**未来做更高自动化版本**，那它们值得作为后续路线保留。

---

## 先把需求说精确：到底要量什么间距

在动手做算法前，至少要把下面 4 个问题定下来。医生的访谈把这 4 件事说得已经比较明确了。

### 1. 要的不是单帧结果，而是一条距离变化曲线

真正交付物至少应该包括：

- 每一帧两个 marker 的位置：`p1(t), p2(t)`
- 每一帧的距离：`d(t) = ||p1(t) - p2(t)||`
- 一条完整的距离时间曲线：`{t, d(t)}`
- 曲线摘要：最大值、最小值、峰峰值、平均值、异常帧标记

这一点和上一版文档最大的差别在于：这里不再是“找到点以后量一次”，而是“从第一帧跟到最后一帧，并把每一帧的距离串起来”。也就是说，**跟踪连续性**本身已经成了问题的一半。

### 2. 输入优先级：DICOM 最好，MP4 可以兜底

从医生的描述看，输入大致分两类：

- **DICOM 造影文件**
  - 最优先，因为通常能保留原始像素、帧序信息以及部分空间信息。
- **MP4 或其他导出视频**
  - 可以做 PoC，但常见问题是压缩、时间轴精度下降、空间元数据缺失。

pydicom 文档说明，可以直接从数据集读取 `pixel_array`，也可以在需要时对像素数据应用 `VOI LUT` 或 windowing 操作，这意味着 DICOM 输入更适合作为算法主入口 [[15]](https://pydicom.github.io/pydicom/stable/guides/user/working_with_pixel_data.html)。

因此，这篇文档后面默认按 **DICOM 优先、视频兜底** 来设计方案。

### 3. 输出单位是什么

这里至少要同时明确两种量纲：

- **像素单位 px**
  - 前期 PoC 最容易先落地，因为不依赖额外标定。
- **时间单位 frame / ms**
  - 医生最终关心的是“距离随时间变化”，所以横轴定义必须明确。
- **物理单位 mm**
  - 如果 DICOM 里有可用空间信息，或者能做可信校准，再升级到毫米结果。

OpenCV 的相机标定教程明确指出，镜头会带来径向畸变和切向畸变；如果直接用未经校正的像素坐标做精确测量，边缘区域误差会更明显 [[1]](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)。

如果输入是 DICOM，多帧图像还可能带有时间相关信息。DICOM 的 `Frame Time Vector` 属性说明，它可以保存多帧图像中每一帧相对前一帧的真实时间增量，单位是毫秒 [[18]](https://dicom.innolitics.com/ciods/ultrasound-multi-frame-image/cine/00181065)。而 `Pixel Spacing (0028,0030)` 则给出相邻像素中心之间的物理距离 [[14]](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_10.7.html)。这两个信息一个决定横轴，一个决定纵轴能不能升级到毫米。

### 4. 初始化是否必须全自动

这类任务里，一个很容易被忽略的现实问题是：**只有两个 marker**。这意味着前期完全没必要一上来就追求“全自动首帧检测”。

- **方案 A：首帧人工点一下两个 marker**
  - 对 PoC 非常划算，风险最低。
- **方案 B：首帧半自动定位，人工确认**
  - 适合后续想减少人工但又不想引入太复杂模型。
- **方案 C：全自动初始化 + 全自动跟踪**
  - 适合进入稳定版本之后再做。

对医生场景来说，先把“首帧点准、后面跟稳、曲线能看”做出来，通常比把 0 人工交互作为第一目标更务实。

---

## 这类问题为什么容易做出“能跑但不稳”的 Demo

前期 Demo 往往在几段样例视频上表现不错，换一批造影序列就开始漂。这里面最核心的麻烦不在“黑点识别”本身，而在**时间连续性**。

### 1. 心跳和呼吸带来的是复合运动

医生已经明确说了，这段影像会跟着心脏搏动和呼吸运动一起动。也就是说，marker 的轨迹通常不是简单平移，而是混合了快慢两种成分：

- 心跳带来的相对快运动
- 呼吸带来的相对慢运动

所以你最后看到的 `d(t)` 曲线，往往本身就会叠加两类变化。这不是算法噪声，而是业务信号的一部分。

### 2. marker 形状稳定，不代表外观稳定

在造影序列里，即便 marker 本体是稳定的，逐帧外观也可能变化：

- 轻微模糊
- 对比度波动
- 局部遮挡
- 压缩噪声
- 周围导管、骨骼或造影剂纹理干扰

这也是为什么“第一帧能找对”不代表“整段都能跟住”。

### 3. 最大风险不是漏检，而是失追和串 ID

这里只有两个 marker，看起来很简单，但恰恰因为目标数很少，一旦某一帧把 A 和 B 搞反，整条曲线的临床解释都会变差。对这个任务来说，**ID 连续性**比“某一帧中心误差小 0.3 px”更重要。

### 4. DICOM 和 MP4 的可用信息差很多

同一段造影内容，如果拿到的是 DICOM，多半还能继续追时间轴、像素数据甚至部分空间信息；如果拿到的是 MP4，通常就只能退回“视频帧 + fps”语义。PoC 阶段两者都能做，但正式分析最好优先 DICOM。

### 5. 没有先定义“失追怎么办”，曲线就不可信

序列任务里最危险的不是“算不出来”，而是“其实已经跟丢了，但系统还在继续输出距离”。常见异常包括：

- 某一帧 marker 暂时看不清
- A/B 两个 marker 局部重叠
- 搜索窗口漂走，后面全程跟错
- 视频压缩导致模板失真
- 只剩一个 marker 稳定可见

如果这些异常不提前定义拒判规则，最后出的 `d(t)` 曲线会看起来很完整，但解释价值很差。

---

## 初步技术方案：先做一个稳妥的六段式流水线

建议把整条链路拆成下面 6 个模块：

  ```text
  DICOM / MP4 输入
    -> 帧序列解码与时间轴读取
    -> 首帧 marker 初始化
    -> 逐帧局部跟踪
    -> 失追恢复与质量控制
    -> 距离曲线生成与平滑
    -> 导出 px / mm 结果与统计摘要
  ```

  这个拆法的好处是，后续你可以逐段替换：

  - 首帧不稳，就换初始化方式
  - 跟踪不稳，就换模板匹配或光流策略
  - 曲线抖动太大，就补平滑和质控
  - 物理量不准，就补 DICOM spacing 或校准

整个系统不会因为一个模块升级而推倒重来。

---

## 一张更接近实施的流程图

  ```text
  DICOM 或 MP4 输入
    -> 解码为连续帧
    -> 读取 Frame Time Vector / fps
    -> 首帧人工或半自动点选两个 marker
    -> 为 marker A / B 建立局部模板与搜索窗
    -> 逐帧跟踪 A / B 位置
    -> 置信度检查与失追恢复
    -> 计算每帧距离 d(t)
    -> 曲线平滑、异常帧标注
    -> 输出距离变化曲线与关键统计量
  ```

  这里最重要的变化是：整条链路的中心从“单帧识别”改成了“序列跟踪”。两 marker 的轨迹如果稳定，后面的距离曲线自然能出来；轨迹一旦断掉，单帧识别再漂亮也没法直接交付给医生。

  从工程实现上看，每一步的中间结果都最好留图或留表。这样排查问题时，不会只知道“结果不对”，而是能明确判断卡在初始化、跟踪、时间轴还是毫米换算。

  这个拆法的好处是，后续你可以逐段替换：

  - 首帧不稳，就换初始化方式
  - 跟踪不稳，就换 template matching / optical flow
  - 曲线抖动大，就补时间平滑和异常剔除
  - 标尺不稳，就退回 px 曲线或补 DICOM 几何信息

整个系统不会因为一个模块升级而推倒重来。

---

## 模块一：序列解码、首帧标准化与 ROI 初始化

### 目标

把医生给的一小段造影文件，先统一整理成**可逐帧处理的帧序列 + 时间轴 + 两个 marker 的初始位置**。

### 推荐做法

- 如果是 DICOM，优先直接读取原始像素帧
- 如果需要显示增强，再对像素数据做 windowing 或 LUT 处理 [[15]](https://pydicom.github.io/pydicom/stable/guides/user/working_with_pixel_data.html)
- 如果是 MP4，先按原 fps 解码，保留帧号顺序
- 在首帧上人工点选或半自动确认两个 marker 中心
- 以两个 marker 为中心建立局部 ROI 和搜索窗

对这道题来说，首帧初始化其实是一个很划算的人工环节。因为目标只有两个点，所以首帧哪怕让医生或工程师点一下，也往往比一开始硬上全自动更稳、更便宜。

### 为什么 DICOM 仍然明显优于 MP4

DICOM 的优势不只是“画质可能更好”，更关键的是它更容易保留像素数据和多帧元信息。pydicom 文档给出的典型流程就是先拿 `pixel_array`，再按需要应用 `apply_modality_lut()` 或 `apply_voi_lut()` [[15]](https://pydicom.github.io/pydicom/stable/guides/user/working_with_pixel_data.html)。而 MP4 更像是最终播放版本，拿来做 PoC 没问题，但一旦进入医学测量语境，很多原始信息都已经丢了。

### 为什么 ROI 很重要

序列跟踪里，ROI 的价值甚至比单帧识别更大。因为跟踪不是每帧都从全图重新搜索，而是希望在**上一帧附近的小区域里继续找到目标**。只要 ROI 控得住，算法面对的是局部细微位移；一旦 ROI 放飞，问题立刻变成全局搜索，稳定性和速度都会掉下来。

对这类医生访谈里描述得很清楚的场景，早期系统完全可以接受“首帧人工点选 + 后续局部跟踪”的策略。目标不是做一个什么视频都能跟的通用 tracker，而是先把医生关心的这类造影片段做稳。

---

## 模块二：首帧 marker 初始化

### 模块二：首帧 marker 初始化——先把 A / B 认准

这一步的目标不是“全图找所有黑点”，而是**先把医生真正关心的那两个 marker 认准**。因为目标数非常少，所以这里最实用的策略往往不是全自动，而是：

- 首帧人工点选两个 marker 的大致中心
- 在局部小 ROI 内做精细定位
- 给这两个点建立各自的模板、编号和搜索窗

如果 marker 在局部区域里对比度足够高，可以直接在小 ROI 中做二值化 + 连通域筛选。OpenCV 的 `connectedComponentsWithStats` 可以同时给出连通域统计量和质心，这很适合在首帧做局部精定位 [[10]](https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html)。

如果 marker 近似圆形，也可以在小范围内用 `SimpleBlobDetector` 做初始化。它本身支持按面积、圆度、颜色等条件过滤 [[4]](https://docs.opencv.org/3.4/d0/d7a/classcv_1_1SimpleBlobDetector.html)，比全图搜索更可控。

### 为什么这里不建议一开始就上全自动检测模型

医生场景里，第一阶段真正要回答的是“能不能把两 marker 的距离变化曲线做出来”。只要这个目标还没被证明，过早把问题升级成“任意造影序列全自动检出两 marker”，很容易把项目推向高成本路线：

- 标注更多
- 调参更多
- 解释更难
- 失追以后更难排查

所以 PoC 最稳的起步方式其实很朴素：**先人工初始化，再自动跟踪**。

---

## 模块三：逐帧跟踪——template matching 与光流是两条主线

这一步才是整道题的核心。首帧点对了，只说明你有了起点；真正决定结果能不能交付的是，后面每一帧能不能继续把 A 和 B 跟住。

### 方案 1：局部 template matching

OpenCV 的模板匹配本质上是拿一个 patch 在搜索区域里滑动，计算每个位置的匹配分数，再用 `minMaxLoc()` 找到最好匹配位置 [[16]](https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html)。

对这个任务来说，它的优点很直接：

- 目标数少
- 首帧模板容易拿到
- 局部搜索窗通常不大
- 输出分数天然能拿来做质控

如果造影序列里 marker 外观变化不大、位移也不夸张，模板匹配通常是最快能起量的一条路。

### 方案 2：Lucas-Kanade 稀疏光流

OpenCV 的 Lucas-Kanade 光流方法可以把“上一帧的点”传进去，返回这些点在下一帧的位移估计。官方说明里提到，它假设局部邻域内像素运动相似，并通过金字塔处理更大位移 [[17]](https://docs.opencv.org/4.x/db/d7f/tutorial_js_lucas_kanade.html)。

这条路特别适合：

- 逐帧位移不算太离谱
- 目标局部纹理还能提供可跟踪信息
- 你希望得到更平滑的轨迹，而不只是逐帧重新搜索

### 更实用的工程组合

真到工程上，我更推荐把两条路组合起来，而不是二选一：

- 用上一帧位置定义小搜索窗
- 先用光流给出位移预测
- 再用模板匹配在预测附近做精定位
- 两者差异太大时，直接标记该帧低置信度

这样做的好处是：光流负责“顺着动”，模板匹配负责“拉回去”。


---

## 模块四：失追恢复与轨迹连续性控制

对医生来说，最怕的不是某一帧误差略大，而是中间某段已经跟丢了，系统却还在继续输出一条看起来很顺的曲线。所以这一模块要解决的是：**什么时候认为已经跟丢？跟丢后怎么办？**

### 1. 哪些信号可以判定“这帧不可信”

比较实用的规则包括：

- 模板匹配分数低于阈值
- 光流返回状态失败
- 本帧位移相对上一帧跳变过大
- 两个 marker 的相对位置突然交换
- 搜索结果跑出合理 ROI 范围

### 2. 跟丢以后怎么恢复

恢复策略建议分三级：

- **一级恢复**：扩大局部搜索窗，再尝试一次
- **二级恢复**：回到上一个高置信度模板，重新做局部匹配
- **三级恢复**：要求人工重新点选，或者把这一段标记为不可判读

这里的原则很简单：宁可有一小段曲线断掉，也不要把错误轨迹强行接上。

### 3. 为什么 A/B 编号一致性要单独看

因为这里只有两个 marker，临床解释很可能默认 A 一直是近端、B 一直是远端，或者一开始医生点的左边就是 A、右边就是 B。如果某个时刻这两个编号被交换，曲线数值可能还“看起来正常”，但意义已经变了。

所以系统内部最好始终维护：

- A 的轨迹
- B 的轨迹
- A/B 当前置信度
- A/B 是否发生潜在串号


---

## 模块五：距离曲线生成——先出原始曲线，再做平滑

对这次医生描述的任务，默认距离定义其实很明确：就是两个 marker 质心之间的**欧氏距离**。也就是说，每帧只需要算：

```text
d(t) = ||p1(t) - p2(t)||
```

这一步建议至少输出三层结果：

- **原始距离曲线**：每帧直接计算的 `d(t)`
- **平滑曲线**：用于辅助观察整体趋势，但不能覆盖原始值
- **质控标签**：标出低置信度帧、缺失帧和人工重置点

### 横轴怎么定

横轴建议按优先级这样处理：

- 如果 DICOM 有 `Frame Time Vector`，就累计得到真实时间轴 [[18]](https://dicom.innolitics.com/ciods/ultrasound-multi-frame-image/cine/00181065)
- 如果没有，但视频 fps 明确，就按固定帧间隔换算
- 如果时间信息也不稳定，至少保留 frame index 版本

### 一个很实际的提醒

这类任务里，不建议一上来就只给医生一条“平滑过的漂亮曲线”。更稳的交付方式是：原始曲线、平滑曲线、关键帧截图一起给。这样医生一眼就能分辨，某个波动到底是生理变化、成像变化，还是算法失追。

---

## 模块六：从像素距离到真实距离

如果最终只看 `px-frame` 语义，这套系统更像一个时序识别工具；如果要升级到 `mm-ms`，它才真正进入医学测量系统的范畴。

### 1. 先把横轴定清楚：frame 还是毫秒

这类任务最容易被低估的不是距离，而是**时间轴**。如果曲线的横轴都不可信，后面的搏动分析和节律解释就会一起打折。

- 如果 DICOM 里能读到 `Frame Time Vector`，优先按真实帧间隔累计时间 [[18]](https://dicom.innolitics.com/ciods/ultrasound-multi-frame-image/cine/00181065)
- 如果拿到的是固定帧率视频，就用 `fps` 近似换算
- 如果时间信息不稳定，至少保留基于 frame index 的版本，避免伪精确

### 2. 再看纵轴：像素距离能不能升级成毫米

最理想的情况是，DICOM 提供了可用的 `Pixel Spacing (0028,0030)`，它表示相邻像素中心之间的物理距离 [[14]](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_10.7.html)。这时可以把每帧的像素距离换成毫米：

```text
d_mm(t) = d_px(t) * spacing
```

但这个升级并不总该默认开启。尤其在导出视频、投影放大关系不清楚，或者医生此阶段只想看趋势时，更稳妥的做法是：

- 先把 `d_px(t)` 做稳
- 再把 `d_mm(t)` 作为增强版输出

### 哪种情况下先不要硬上毫米结果

- 只有 MP4，没有可追溯空间信息
- DICOM 有图像，但 spacing 语义和当前投影场景仍不明确
- 这轮更关心相对变化趋势，而不是绝对长度

### 误差分析：别只盯着单帧中心点

时序跟踪里，最终误差往往不是某一帧没点准，而是多个环节叠加后的结果。前期可以先用一个足够工程化的视角来看：

```text
e_total ≈ sqrt(e_init^2 + e_track^2 + e_id^2 + e_time^2 + e_scale^2)
```

| 误差源 | 常见表现 | 优先缓解手段 |
|------|------|------|
| 首帧初始化偏差 | 整条曲线整体偏移 | 首帧人工确认，必要时做局部精定位 |
| 跟踪漂移 | 曲线缓慢偏离肉眼观察结果 | 小搜索窗 + 光流预测 + 模板回拉 [[16]](https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html) [[17]](https://docs.opencv.org/4.x/db/d7f/tutorial_js_lucas_kanade.html) |
| 串 ID | 曲线局部出现不合常理的跳变 | 单独维护 A/B 编号和相对位置约束 |
| 时间轴误差 | 波峰间隔和生理节律对不上 | 优先用 DICOM 时间信息，其次才是 fps |
| 标尺不确定 | px 能看趋势，mm 却不敢解释 | 没把握时先只交付 px 曲线 |

对医生业务来说，前期比“绝对值是不是已经很准”更值得先盯住的是**轨迹连续性和重复性**。如果同一段序列重复跑几次，`d(t)` 曲线形态都差不多，再谈毫米化会顺得多。

---

## 一个可执行的 MVP 方案

如果现在要的是“先证明能不能做”，我会建议从下面这个最小版本开始：

### 第 1 版：先把 `d(frame)` 跑出来

技术栈：

- OpenCV
- Python
- 少量 NumPy

步骤：

1. 读取 DICOM 或 MP4
2. 首帧人工点选两个 marker
3. 为 A / B 建立局部模板
4. 在后续每一帧的小搜索窗里做模板匹配
5. 输出原始距离曲线 `d(frame)`
6. 同时导出关键帧截图和匹配分数

这一步的目标不是高精度，而是确认：

- 两个 marker 能不能跟完整段序列
- 明显失追能不能被识别出来
- 曲线走势是否符合肉眼观察

### 第 2 版：把 `d(frame)` 升级成 `d(t)`

在第 1 版基础上补：

- Lucas-Kanade 光流预测 [[17]](https://docs.opencv.org/4.x/db/d7f/tutorial_js_lucas_kanade.html)
- 模板匹配精定位 [[16]](https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html)
- 低置信度帧标记
- DICOM 时间轴或 fps 换算

### 第 3 版：把趋势曲线升级成测量报告

继续补：

- `Pixel Spacing` 或可信校准
- `d_mm(t)` 输出
- 平滑曲线与原始曲线并排展示
- 峰值、谷值、峰峰值和可疑帧报告

这个三段式推进的好处是：先证明“能跟住”，再证明“时间轴可信”，最后才证明“毫米结果可解释”。

---

## 一个简化的 OpenCV 实现骨架

下面这段代码不是完整生产代码，但足够表达系统怎么搭起来：

```python
import cv2
import numpy as np


def extract_patch(gray, center, radius=12):
    x, y = map(int, center)
    return gray[y - radius:y + radius + 1, x - radius:x + radius + 1].copy()


def track_with_template(gray, template, center, search_radius=20):
    x, y = map(int, center)
    h, w = template.shape[:2]
    x1 = max(0, x - search_radius)
    y1 = max(0, y - search_radius)
    x2 = min(gray.shape[1], x + search_radius + w)
    y2 = min(gray.shape[0], y + search_radius + h)
    search = gray[y1:y2, x1:x2]

    score_map = cv2.matchTemplate(search, template, cv2.TM_CCOEFF_NORMED)
    _, score, _, max_loc = cv2.minMaxLoc(score_map)
    cx = x1 + max_loc[0] + w / 2.0
    cy = y1 + max_loc[1] + h / 2.0
    return np.array([cx, cy], dtype=np.float32), float(score)


def track_marker_sequence(frames, p1_init, p2_init):
    prev_gray = frames[0]
    p1 = np.array(p1_init, dtype=np.float32)
    p2 = np.array(p2_init, dtype=np.float32)
    tmpl1 = extract_patch(prev_gray, p1)
    tmpl2 = extract_patch(prev_gray, p2)

    tracks = []
    for idx, gray in enumerate(frames):
        p1, s1 = track_with_template(gray, tmpl1, p1)
        p2, s2 = track_with_template(gray, tmpl2, p2)
        dist = float(np.linalg.norm(p1 - p2))
        tracks.append({
            "frame": idx,
            "p1": p1.copy(),
            "p2": p2.copy(),
            "distance_px": dist,
            "score1": s1,
            "score2": s2,
        })
        prev_gray = gray

    return tracks
```

  这段骨架体现了三件事：

  - 先有首帧初始化，再谈后续自动跟踪
  - 每一帧都要保留位置和置信度
  - 距离曲线其实是轨迹结果的派生物，不是独立模块

  如果要把这段骨架继续往工程代码推进，推荐至少拆成下面 6 个模块：

  ```text
  image_io.py        # DICOM / MP4 解码、时间轴读取
  init_marker.py     # 首帧点选、局部精定位
  tracking.py        # template matching / optical flow
  quality_gate.py    # 失追检测、低置信度标记、串 ID 检查
  metrics.py         # distance_px / distance_mm / 峰峰值统计
  report.py          # 曲线导出、关键帧截图、结果摘要
  ```

  `OpenCV` 参数调试顺序也尽量固定，不然很容易多变量一起联动：

  1. 先固定首帧初始化方式
  2. 再调搜索窗大小和模板尺寸
  3. 再调模板匹配阈值与低分告警阈值 [[16]](https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html)
  4. 再调光流窗口、金字塔层数和失败判定 [[17]](https://docs.opencv.org/4.x/db/d7f/tutorial_js_lucas_kanade.html)
  5. 最后才调曲线平滑和异常剔除规则

  对只有两个 marker 的序列任务来说，最值钱的不是把每个局部视觉小问题都解到极致，而是让系统能明确地告诉你：哪几帧可信，哪几帧已经不该继续自动输出。

  ---

  ## 方案选型建议：不同阶段别用同一把锤子

| 阶段 | 推荐方案 | 优点 | 风险 |
|------|----------|------|------|
| 快速验证 | 首帧人工点选 + 局部模板匹配 | 上手快、可解释、最接近医生真实使用 | 对外观变化敏感 |
| 稳定版本 | 光流预测 + 模板精定位 + 失追恢复 | 兼顾连续性与稳健性 | 实现复杂度中等 |
| 增强版本 | DICOM 时间轴 + Pixel Spacing + 报告导出 | 更适合真正测量和回顾分析 | 依赖输入质量和元数据 |
| 高复杂背景 | 学习型 detector + tracking-by-detection | 对复杂遮挡更有潜力 | 数据标注和维护成本高 |

多数项目一开始没必要上深度学习。只有在下面这些情况同时出现时，learning-based 方法才值得优先考虑：

- marker 外观变化非常大
- 遮挡频繁
- 模板匹配和光流都经常失效
- 你已经有稳定的数据标注来源

---

## 落地时最该盯住的 4 个指标

### 1. 轨迹完整率

从第一帧到最后一帧，A/B 两条轨迹有多少比例是连续且可用的。这个指标直接决定曲线是不是完整。

### 2. 低置信度帧比例

如果低分帧很多，说明系统没有真正把局部跟踪做稳，哪怕曲线还能画出来，也要谨慎解释。

### 3. 串 ID 率

即便两 marker 都找到了，只要 A/B 交换过一次，曲线的临床语义就会被污染。这个指标经常比中心点误差更重要。

### 4. 曲线重复性

同一段序列重复运行几次，曲线形态和关键统计量波动多大。序列任务里，这比某一帧偶尔“点得特别准”更值钱。

从交付角度看，这 4 个指标比“单帧截图上圆心画得多漂亮”更能判断方案能不能进入医生工作流。

---

## 我的初步判断：这题大概率能用传统视觉先做出来

如果场景满足下面这些条件：

- marker 在局部区域里对比度还可以
- 每帧位移不是特别夸张
- 允许首帧人工点选
- 先接受 px 或 frame 级结果
- 输入优先能拿到 DICOM 或高质量视频

那这题完全有机会先用传统视觉打通，不必第一步就上模型。

一套比较稳妥的起步组合是：

- 首帧人工初始化
- 小搜索窗模板匹配
- 光流做位移预测
- 低置信度帧标记
- 原始 `d(frame)` 曲线输出
- 后续再补时间轴和毫米换算

如果我要排优先级，我会这样排：

1. 先把**测量定义**定清楚
2. 再把**两 marker 持续跟住**做稳
3. 再把**时间轴和异常帧**标清楚
4. 最后才是**毫米级精度**

顺序反了，项目很容易陷入“毫米还没算明白，但轨迹其实已经跟丢”的混乱状态。

---

## 总结与延伸

这次医生把需求说清楚以后，问题本质已经变成了**心脏造影序列中的双 marker 时序跟踪**。真正要解决的不是某个单点检测算法，而是一条完整链路：

- 先明确交付物是 `d(t)` 曲线，而不是单帧距离
- 用 DICOM / MP4 解码和首帧初始化确定起点
- 用 template matching / optical flow 把两 marker 逐帧跟住
- 用质控和失追恢复保证曲线不被伪结果污染
- 用时间轴和 Pixel Spacing 决定它能不能升级成测量结果
- 用异常规则和统计摘要把结果变成医生可读的数据

如果只是做前期验证，建议先跑通首帧人工初始化 + 自动跟踪 + `d(frame)` 曲线；如果要进入正式测量，再补时间轴、空间标尺和报告化输出。这条路线投入克制，但非常贴近医生实际使用场景。

---

## 采集侧约束：别让算法替硬件背锅

同样一套算法，为什么在实验室里能跑，在现场却经常飘？很多时候不是算法退化，而是采集链路没有被当成测量系统的一部分。

前期 PoC 阶段，建议优先把下面几件事管住：

- **优先保留 DICOM 原始导出**
  - 一旦只剩二次压缩视频，时间轴和空间信息都会打折。
- **尽量避免再压缩**
  - MP4 能用，但最好保留原分辨率和原帧率，不要反复转码。
- **首帧 marker 要清楚可见**
  - 因为整条轨迹都从这里起步，起点模糊会把后面全部拖偏。
- **尽量别让 marker 频繁出视野**
  - 对跟踪任务来说，目标短暂遮挡可以恢复，长期出框就很难自动续上。
- **让 marker 占够像素**
  - 如果 marker 只有 2 到 3 个像素宽，再好的跟踪器也很难稳定输出可信曲线。

这一步没有什么“高级算法”可替代，本质上是在给后面的时序跟踪争取信噪比。

## 什么时候值得上亚像素定位

如果系统最终只输出趋势和粗分档，像素级中心点通常已经够用。但当下面任一情况出现时，就该认真考虑亚像素：

- 单个像素误差已经接近你的业务容差
- 同一段序列重复计算时，曲线在 1 px 左右来回抖
- marker 中心的位置会直接影响最终判定阈值
- 你已经完成了标定，下一步瓶颈明显落在点位精度上

OpenCV 提供了 `cornerSubPix`，其目标就是把点位从整数像素细化到更精确的位置 [[9]](https://docs.opencv.org/4.x/dd/d92/tutorial_corner_subpixels.html)。虽然它直接面向角点，但工程启发很明确：当测量问题开始被 1 个像素的量化误差卡住时，定位方法就不能只停在整数像素网格上。

对 marker 跟踪问题，更常见的亚像素路线有三种：

- **灰度重心细化**
  - 先拿到二值连通域，再在原始灰度图里做局部加权质心。
- **椭圆 / 圆模型拟合**
  - 对轮廓点做拟合，用几何中心替代像素中心。
- **局部曲面拟合**
  - 在 marker 附近拟合灰度分布，再求极值点或对称中心。

如果现在还是 PoC 阶段，我更建议先把像素级流程做稳，再挑一批高价值样本做亚像素对比实验，而不是过早把整条链路复杂化。

## 异常样本处理：上线前就该定规则

工程系统最怕“算法算了一个值，但这个值根本不可信”。所以异常判定最好和测量流程一起设计。

| 异常情况 | 常见表现 | 建议处理 |
|------|------|------|
| 某一帧 marker 暂时不可见 | 距离突然跳高或跳低 | 标记该帧低置信度，不强行补出高精度结果 |
| 两个 marker 过近或重叠 | A/B 位置交换风险上升 | 触发串 ID 检查，必要时中断该段 |
| marker 跑到视野边缘 | 搜索窗被截断 | 标记为即将失追，扩大搜索窗或人工重置 |
| 视频压缩过重 | 模板匹配分数持续偏低 | 回退到 px/frame 级结果，降低自动化期望 |
| 时间信息缺失 | 曲线横轴不可信 | 至少保留 frame index 版本，并显式说明限制 |

一个很实用的原则是：**宁可这张图返回“不可判定”，也别输出一个看起来很精确、实际上没意义的数。**

## PoC 阶段怎么验收，才不会陷入“演示好看、上线翻车”

如果只是为了证明可行性，验收不需要一步到位，但必须覆盖足够多的扰动条件。

建议在 PoC 阶段至少准备下面几类样本：

- **标准样本**：DICOM 清晰、两 marker 全程可见、运动幅度中等
- **弱干扰样本**：轻微模糊、轻微呼吸位移变化、轻微压缩
- **异常样本**：短时遮挡、边缘出框、局部重叠、低分片段
- **边界样本**：最小 marker 尺寸、最低对比度、最快运动段

验收时建议至少看 4 项：

- **轨迹连续率**：A/B 两条轨迹有没有断得太厉害
- **低置信度帧识别能力**：系统会不会把坏帧伪装成好帧
- **曲线重复性**：同一段序列重复跑几次结果稳不稳
- **异常拒判能力**：明显坏段能不能被系统拦下来

如果项目最终要走到量产，一个很好的里程碑不是“某 3 张图测得很准”，而是：

```text
标准样本稳定输出 d(frame)
  -> 弱干扰样本仍能保持轨迹连续
  -> 异常样本可以拒判或打低置信度标签
  -> 高质量 DICOM 才升级到 d(t) / d_mm(t)
```

这条验收线虽然朴素，但很接近真实项目从 PoC 走向上线的节奏。

---

## 两个更具体的落地案例

### 案例一：DICOM 清晰、两 marker 全程可见、位移中等

这是最好做的一类。

推荐链路：

- 首帧人工初始化
- 局部模板匹配
- 光流预测做平滑跟随
- 输出原始 `d(frame)` 与关键帧截图
- 再根据 DICOM 时间信息升级到 `d(t)`

这类场景的重点不是“能不能识别”，而是尽快把一条医生看得懂、愿意拿来讨论的距离曲线做出来。

### 案例二：只有 MP4、压缩明显、marker 有短时遮挡

这是更接近现实流转文件的一类。

推荐链路：

- 先保住分辨率和 fps 信息
- 首帧人工初始化仍然保留
- 搜索窗适当放大，降低过度乐观的自动化预期
- 只交付 `px-frame` 曲线，不急着解释毫米值
- 对低分片段直接打标签，不把整段说成“连续可信”

这类场景里，系统的核心能力不是“每段视频都给完美曲线”，而是“能把可信段和不可信段分清楚”。

---

## 最后的收束

回到医生最初的问题：给一段会跟着心跳和呼吸一起动的造影序列，能不能把两个 marker 盯住，并输出从开头到结尾的距离变化情况。真正靠谱的路径，并不是直接找一个“最强检测算法”，而是把它拆成一条可控的时序测量链：

- 用 DICOM / MP4 解码确定帧和时间轴
- 用首帧初始化把 A/B 的身份定下来
- 用局部跟踪把两 marker 持续跟住
- 用质控把失追和串号挡在结果外面
- 用 spacing 或校准决定能不能升级成毫米曲线

如果场景稳定、marker 对比度足够，这类问题大概率可以先用传统视觉做出一个可信的 PoC。真正决定项目成败的，往往不是算法名词有多新，而是输入格式、时间轴、异常规则和交付口径有没有一开始就想清楚。

---

## 参考来源

| 编号 | 来源 | 说明 |
|------|------|------|
| 1 | [OpenCV 官方文档 - Camera Calibration](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) | 相机畸变、内外参与去畸变基础 |
| 2 | [OpenCV 官方文档 - Image Thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html) | 自适应阈值、Otsu 阈值及噪声场景说明 |
| 3 | [KEYENCE - What is Blob Analysis in Machine Vision?](https://www.keyence.com/products/vision/vision-sys/resources/guides/what-is-blob-analysis-in-machine-vision.jsp) | 工业视觉中 Blob 分析的流程与测量应用 |
| 4 | [OpenCV 官方文档 - cv::SimpleBlobDetector](https://docs.opencv.org/3.4/d0/d7a/classcv_1_1SimpleBlobDetector.html) | Blob 检测算法流程及参数过滤项 |
| 5 | [OpenCV 官方文档 - Hough Circle Transform](https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html) | 圆检测的基本原理与适用条件 |
| 6 | [scikit-image 官方文档 - Skeletonize](https://scikit-image.org/docs/stable/auto_examples/edges/plot_skeleton.html) | 骨架 / 中轴与局部宽度估计思路 |
| 7 | [SciPy 官方文档 - Interpolation (scipy.interpolate)](https://docs.scipy.org/doc/scipy/tutorial/interpolate.html) | 样条拟合与插值方法选型 |
| 8 | [OpenCV 官方文档 - Contour Features](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html) | 最小外接圆、椭圆拟合、直线拟合等轮廓特征 |
| 9 | [OpenCV 官方文档 - Detecting corners location in subpixels](https://docs.opencv.org/4.x/dd/d92/tutorial_corner_subpixels.html) | 亚像素定位的基本思路与 API |
| 10 | [OpenCV 官方文档 - Structural Analysis and Shape Descriptors](https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html) | 连通域统计、形状分析等基础 API |
| 11 | [OpenCV 官方文档 - Morphological Transformations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html) | 开闭运算、形态学梯度等基础形态学操作 |
| 12 | [OpenCV 官方文档 - Image Segmentation with Watershed Algorithm](https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html) | marker-based watershed 与粘连对象分离思路 |
| 13 | [Edmund Optics - Telecentric Design Topics](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/telecentric-design-topics/) | 远心镜头与透视 / 视差控制的测量意义 |
| 14 | [DICOM Standard - Basic Pixel Spacing Calibration Macro](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_10.7.html) | `Pixel Spacing (0028,0030)` 的物理含义 |
| 15 | [pydicom 官方文档 - Working with Pixel Data](https://pydicom.github.io/pydicom/stable/guides/user/working_with_pixel_data.html) | DICOM `pixel_array`、VOI LUT 与像素处理入口 |
| 16 | [OpenCV 官方文档 - Template Matching](https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html) | 模板匹配、滑窗搜索与匹配分数 |
| 17 | [OpenCV 官方文档 - Optical Flow](https://docs.opencv.org/4.x/db/d7f/tutorial_js_lucas_kanade.html) | Lucas-Kanade 稀疏光流与金字塔处理 |
| 18 | [DICOM Standard Browser - Frame Time Vector Attribute](https://dicom.innolitics.com/ciods/ultrasound-multi-frame-image/cine/00181065) | 多帧图像中逐帧时间增量的定义 |
| 19 | [ImageJ / Fiji - TrackMate](https://imagej.net/plugins/trackmate/) | 通用轨迹分析、结果编辑与 spot / cell tracking 工具 |
| 20 | [3D Slicer 文档 - Sequences](https://slicer.readthedocs.io/en/latest/user_guide/modules/sequences.html) | DICOM / 时序节点浏览、回放与 Sequence node 支持 |
| 21 | [Ultralytics 文档 - Track Mode](https://docs.ultralytics.com/modes/track/) | YOLO 的 tracking 模式、BoT-SORT / ByteTrack 与可配置 tracker |
| 22 | [MMTracking 文档 - Introduction](https://mmtracking.readthedocs.io/en/dev-1.x/overview.html) | OpenMMLab 视频感知工具箱，对 `SOT/MOT/VID/VIS` 的统一支持 |

