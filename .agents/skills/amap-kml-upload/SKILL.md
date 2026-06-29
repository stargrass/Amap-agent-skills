---
name: amap-kml-upload
description: 将地址清单上传至高德地图小程序(wia.amap.com)。适用于需要将地理位置数据批量导入高德地图的场景。支持KML格式，需选择"谷歌地图"作为数据来源。
---

# 高德地图地址清单上传

## 概述

本Skill用于将地理位置清单转化为KML格式的地理位置文件上传，并至高德地图小程序平台(wia.amap.com)，实现地点数据的批量导入和可视化管理。

## 快速开始

**最简单的使用方式：**

直接向Agent输入需要导入的地址列表，例如：

```
把以下地址导入高德地图小程序：上海市：武康大楼、人民广场、一大会址、外滩
```

Agent会自动完成以下步骤：
1. 查询每个地址的坐标信息
2. 进行坐标系转换（GCJ-02 → WGS-84）
3. 生成KML文件
4. 上传到高德地图小程序
5. 返回导入结果

**您也可以：**
- 提供已有的KML文件直接上传
- 提供CSV或Excel格式的位置数据
- 指定地图名称和描述信息

## 地址确认规则

**重要：当查询地址不清晰或存在多个结果时，必须向用户询问并确认**

### 需要确认的情况

1. **地址不明确**
   - 例如："人民广场" 可能指多个城市的人民广场
   - 应询问："您指的是哪个城市的人民广场？上海、北京还是其他城市？"

2. **存在多个匹配结果**
   - 例如："万达广场" 在全国有多个分店
   - 应列出选项："找到以下3个万达广场，请选择：
     - 上海五角场万达广场
     - 上海周浦万达广场
     - 上海江桥万达广场"

3. **地址信息不完整**
   - 例如："星巴克" 没有具体位置
   - 应询问："请提供更具体的地址，如'星巴克（南京东路店）'或'星巴克（徐汇区XX路）'"

### 确认方式

使用 `AskUserQuestion` 工具向用户展示选项，让用户选择正确的地址。

## 前置条件

1. 用户已在高德地图小程序(wia.amap.com)完成登录
2. KML文件已准备好，使用WGS-84坐标系（标准GPS坐标）
3. 如使用GCJ-02坐标系（高德/百度坐标），需先转换为WGS-84

## 浏览器操作工具说明

本Skill使用 **Playwright MCP** 进行网页自动化操作。所有网页交互通过以下 Playwright MCP 工具完成：

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `browser_navigate` | 导航到指定URL | `url` |
| `browser_snapshot` | 获取页面可访问性快照（用于定位元素） | 无必填参数 |
| `browser_click` | 点击页面元素 | `target`（元素ref或选择器）, `element`（元素描述） |
| `browser_type` | 在输入框中输入文本 | `target`, `text` |
| `browser_file_upload` | 上传文件 | `paths`（文件绝对路径数组） |
| `browser_select_option` | 选择下拉框选项 | `target`, `values` |
| `browser_wait_for` | 等待文本出现/消失或等待指定时间 | `text`, `textGone`, `time` |
| `browser_take_screenshot` | 页面截图 | `type`（png/jpeg）, `filename` |
| `browser_fill_form` | 批量填写表单字段 | `fields`（字段数组） |
| `browser_handle_dialog` | 处理浏览器弹窗 | `accept`（是否接受） |

### 核心操作模式

**定位元素**：每次操作前，先调用 `browser_snapshot` 获取页面快照，从返回的元素树中找到目标元素的 `ref` 标识，然后在后续操作中使用该 `ref` 作为 `target` 参数。

```
# 1. 先获取快照，定位元素
browser_snapshot()
# 返回结果中包含类似: button "创建新地图" [ref=e5]

# 2. 使用 ref 进行操作
browser_click(target="e5", element="创建新地图按钮")
```

**上传文件**：先点击上传区域触发文件选择器，再调用 `browser_file_upload`。

```
# 1. 点击上传区域触发文件选择对话框
browser_click(target="<上传区域的ref>", element="上传区域")
# 2. 上传文件
browser_file_upload(paths=["/absolute/path/to/file.kml"])
```

## 坐标转换与KML生成

本Skill内置了坐标转换脚本，位于 `assets/gcj02_to_wgs84_kml.py`。

### 使用方法

使用内置脚本快速生成KML文件：

```bash
# 单个地点
python assets/gcj02_to_wgs84_kml.py \
    --name "地点名称" \
    --lng 121.427373 \
    --lat 31.256076 \
    --output locations.kml

# 多个地点
python assets/gcj02_to_wgs84_kml.py \
    --name "地点1" --lng 121.427373 --lat 31.256076 \
    --name "地点2" --lng 103.868172 --lat 36.039613 \
    --name "地点3" --lng 114.157674 --lat 22.282416 \
    --output locations.kml

# 带地址描述
python assets/gcj02_to_wgs84_kml.py \
    --name "你说了算牛味馆" --lng 121.427373 --lat 31.256076 --address "华池路84号" \
    --name "金强牛肉面" --lng 103.868172 --lat 36.039613 --address "定西路7-19号" \
    --map-name "地点搜索" \
    --output locations.kml
```

### 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--name` | 地点名称（可多次使用） | 是 |
| `--lng` | GCJ-02经度（可多次使用） | 是 |
| `--lat` | GCJ-02纬度（可多次使用） | 是 |
| `--address` | 地址描述（可选） | 否 |
| `--output` | 输出KML文件名 | 否，默认locations.kml |
| `--map-name` | 地图名称 | 否，默认"地图名称" |
| `--description` | 地图描述 | 否，默认"描述信息" |

### 手动转换代码

如需在代码中直接调用转换函数：

```python
from assets.gcj02_to_wgs84_kml import gcj02_to_wgs84, generate_kml

# 转换单个坐标
wgs84_lng, wgs84_lat = gcj02_to_wgs84(121.427373, 31.256076)

# 批量生成KML
locations = [
    {"name": "地点1", "gcj_lng": 121.427373, "gcj_lat": 31.256076, "address": "地址1"},
    {"name": "地点2", "gcj_lng": 103.868172, "gcj_lat": 36.039613, "address": "地址2"},
]
generate_kml(locations, output_file="locations.kml")
```

## KML文件格式

标准KML格式示例：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>地图名称</name>
    <description>描述信息</description>
    
    <Placemark>
      <name>地点名称</name>
      <description>地点描述</description>
      <Point>
        <coordinates>经度,纬度,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>
```

## 操作步骤

> **重要**：每一步操作前都需要先调用 `browser_snapshot` 获取当前页面状态，根据快照中的元素 `ref` 进行后续操作。

### 步骤1：导航到高德地图小程序

```
browser_navigate(url="https://wia.amap.com/")
```

等待页面加载完成：
```
browser_wait_for(time=3)
```

### 步骤2：确认用户已登录

调用 `browser_snapshot` 检查页面内容：
```
browser_snapshot()
```

- 如果快照中出现登录相关的元素（如"登录"按钮、手机号输入框等），说明用户未登录，应提示用户手动完成登录后再继续。
- 如果页面正常显示用户内容，则继续下一步。

### 步骤3：创建新地图

1. 通过快照找到"创建新地图"按钮的 ref：
```
browser_snapshot()
```

2. 点击"创建新地图"按钮：
```
browser_click(target="<创建新地图按钮的ref>", element="创建新地图按钮")
```

3. 找到地图名称输入框并输入名称：
```
browser_snapshot()
browser_type(target="<名称输入框的ref>", text="地图名称", element="地图名称输入框")
```

4. 点击"创建"按钮：
```
browser_snapshot()
browser_click(target="<创建按钮的ref>", element="创建按钮")
```

### 步骤4：进入地图编辑页面

导航到地图URL：
```
browser_navigate(url="https://wia.amap.com/#/map?orgId={orgId}&workMapId={workMapId}")
```

等待页面加载：
```
browser_wait_for(time=3)
```

### 步骤5：打开批量导入对话框

通过快照找到"批量导入"按钮并点击：
```
browser_snapshot()
browser_click(target="<批量导入按钮的ref>", element="批量导入按钮")
```

等待对话框出现：
```
browser_wait_for(time=2)
```

### 步骤6：选择数据来源

**关键步骤**：必须选择"谷歌地图"作为数据来源，否则KML文件可能无法识别。

1. 获取快照，找到数据来源下拉框：
```
browser_snapshot()
```

2. 点击下拉框展开选项（默认显示"高德地图(推荐)"）：
```
browser_click(target="<下拉框的ref>", element="数据来源下拉框")
```

3. 等待选项出现，然后选择"谷歌地图"：
```
browser_wait_for(text="谷歌地图")
browser_snapshot()
browser_click(target="<谷歌地图选项的ref>", element="谷歌地图选项")
```

### 步骤7：上传KML文件

1. 获取快照，找到上传区域：
```
browser_snapshot()
```

2. 点击上传区域，触发文件选择对话框：
```
browser_click(target="<上传区域的ref>", element="KML文件上传区域")
```

3. 文件选择对话框弹出后，上传KML文件：
```
browser_file_upload(paths=["/absolute/path/to/locations.kml"])
```

> **注意**：`paths` 必须是文件的**绝对路径**。

### 步骤8：等待导入完成

等待页面显示导入成功提示：
```
browser_wait_for(text="成功导入")
```

如果等待超时，获取快照检查状态：
```
browser_snapshot()
```
- 如果看到"不支持"相关文字，说明文件格式有误，需确认是否选择了"谷歌地图"作为数据来源。
- 可以截图让用户查看当前状态：
```
browser_take_screenshot(type="png", filename="upload_status.png")
```

### 步骤9：完成导入

找到并点击"完成"按钮：
```
browser_snapshot()
browser_click(target="<完成按钮的ref>", element="完成按钮")
```

## 注意事项

1. **坐标系**：KML文件必须使用WGS-84坐标系，如使用GCJ-02需先转换
2. **数据来源**：必须选择"谷歌地图"选项才能正确解析KML文件
3. **文件格式**：支持xls、xlsx、kml、ovkml、csv格式
4. **文件大小**：每次上传不超过50000行，文件大小不超过20M
5. **重复数据**：位置编码相同的数据会被识别为重复数据

## 常见问题

### Q: 上传时显示"不支持的文件格式"？
A: 请确保选择了"谷歌地图"作为数据来源，而不是默认的"高德地图(推荐)"。

### Q: 坐标位置偏差很大？
A: 可能是坐标系问题。高德地图API返回的是GCJ-02坐标，需要转换为WGS-84后再写入KML文件。

### Q: 如何批量查询多个地址的坐标？
A: 可以使用高德地图geo API批量查询，然后进行坐标转换，最后生成KML文件。

## 查看导入结果

**导入成功后，请按以下步骤查看：**

1. 打开高德地图APP
2. 点击底部"我的"标签
3. 进入"地图小程序"
4. 找到您上传的地图名称
5. 点击即可查看所有导入的位置点，并支持随时导航到这些地点

**提示：** 导入的位置数据会同步到您的高德地图账户，可以在手机端和网页端随时访问和使用导航功能。
