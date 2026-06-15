# Agent Skills Collection

这是一个Lingma Agent Skills集合，提供自动化工具和生产力增强功能。

## 可用Skills

### amap-kml-upload - 高德地图KML文件上传

将位置数据批量导入高德地图小程序的自动化工具。

#### 功能特点

- 支持自然语言输入地址列表
- 自动查询地址坐标并进行坐标系转换（GCJ-02 → WGS-84）
- 生成标准KML文件
- 浏览器自动化上传到高德地图小程序
- 支持KML、CSV、Excel等多种格式

#### 使用方法

**方式1：自然语言输入（推荐）**

直接向Agent输入需要导入的地址：

```
把以下地址导入高德地图小程序：武康大楼、人民广场、一大会址、外滩
```

**方式2：指定已有KML文件**

```
把这个KML文件上传到高德地图小程序：locations.kml
```

**方式3：使用Python脚本生成KML**

```bash
python .agents/skills/amap-kml-upload/assets/gcj02_to_wgs84_kml.py \
    --name "地点1" --lng 121.427373 --lat 31.256076 \
    --name "地点2" --lng 103.868172 --lat 36.039613 \
    --output locations.kml
```

#### 查看导入结果

1. 打开高德地图APP
2. 点击底部"我的"标签
3. 进入"地图小程序"
4. 找到您上传的地图名称
5. 点击查看所有位置点，支持随时导航

#### 注意事项

- KML文件必须使用WGS-84坐标系
- 上传时必须选择"谷歌地图"作为数据来源
- 支持xls、xlsx、kml、ovkml、csv格式
- 每次上传不超过50000行，文件大小不超过20M

## 项目结构

```
.
├── .agents/skills/
│   └── amap-kml-upload/
│       ├── SKILL.md                      # Skill详细文档
│       ├── assets/
│       │   └── gcj02_to_wgs84_kml.py    # 坐标转换脚本
│       └── mobile_automation.py          # 移动端自动化脚本
├── shanghai_transport_locations.csv      # 示例CSV文件
├── shanghai_transport_locations.kml      # 示例KML文件
└── README.md                             # 本文件
```

## 许可证

MIT License
