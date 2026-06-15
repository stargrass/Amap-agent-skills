# Agent上传搜索地址到高德地图skill

用于将旅游目标地、美食店铺清单、现场走访地点等地址通过agent导入高德地图中，方便在地图中浏览和导航。

## amap-kml-upload - 高德地图地址上传

将位置数据批量导入高德地图小程序的自动化工具。

### 前置准备

1. **高德地图账号**
   - 确保您已注册高德地图账号
   - 在高德地图小程序（wia.amap.com）完成登录，Agent一般会提示完成

2. **高德地图Web API Key**（用于地址坐标查询）
   - 访问 [高德开放平台](https://console.amap.com/dev/key/app)
   - 创建新应用并获取Web服务API Key
   - 在Agent环境中配置API Key（如需要）
   - 注意：部分Agent可能内置了API Key，无需手动配置

3. **Agent环境**
   - Agent支持浏览器自动化功能（已在Qoder测试）

4. **地址信息准备**
   - 准备好需要导入的地址列表
   - 可以是地名、景点、店铺名称等
   - 建议提供具体的城市信息以提高准确性

5. **Python环境**（如需手动生成KML）
   - Python 3.6+
   - 无需额外依赖库（使用标准库）

### 功能特点

- 支持自然语言输入地址列表
- 自动查询地址坐标并进行坐标系转换（GCJ-02 → WGS-84）
- 生成标准KML文件
- 浏览器自动化上传到高德地图小程序

### 使用方法

**方式1：自然语言输入（推荐）**

直接向Agent输入需要导入的地址：

```
把以下地址导入高德地图小程序：武康大楼、人民广场、一大会址、外滩
```

**方式2：指定已有KML文件**

```
把这个KML文件上传到高德地图小程序：locations.kml
```

### 查看导入结果

1. 打开高德地图APP
2. 点击底部"我的"标签
3. 进入"地图小程序"
4. 找到您上传的地图名称
5. 点击查看所有位置点，支持随时导航

### 注意事项

- 如使用方式2，KML文件必须使用WGS-84坐标系
- 上传时必须选择"谷歌地图"作为数据来源
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
