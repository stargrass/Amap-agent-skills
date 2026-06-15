#!/usr/bin/env python3
"""
GCJ-02坐标转WGS-84并生成KML文件

用法:
    python gcj02_to_wgs84_kml.py --name "地点名称" --lng 经度 --lat 纬度 [--name "地点2" --lng 经度2 --lat 纬度2 ...] --output locations.kml

示例:
    python gcj02_to_wgs84_kml.py \
        --name "你说了算牛味馆" --lng 121.427373 --lat 31.256076 \
        --name "金强牛肉面" --lng 103.868172 --lat 36.039613 \
        --output locations.kml
"""

import math
import argparse
import sys

pi = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323

def transform_lat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def transform_lng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def gcj02_to_wgs84(lng, lat):
    """将GCJ-02坐标转换为WGS-84坐标"""
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    wgs84_lat = lat * 2 - mglat
    wgs84_lng = lng * 2 - mglng
    return wgs84_lng, wgs84_lat

def generate_kml(locations, map_name="地图名称", description="描述信息", output_file="locations.kml"):
    """生成KML文件"""
    kml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{map_name}</name>
    <description>{description}</description>
'''

    for loc in locations:
        name = loc.get("name", "未命名地点")
        address = loc.get("address", "")
        gcj_lng = loc.get("gcj_lng")
        gcj_lat = loc.get("gcj_lat")

        if gcj_lng is None or gcj_lat is None:
            print(f"警告: 地点 '{name}' 缺少坐标信息，已跳过")
            continue

        wgs84_lng, wgs84_lat = gcj02_to_wgs84(gcj_lng, gcj_lat)
        kml_content += f'''    <Placemark>
      <name>{name}</name>
      <description>{address}</description>
      <Point>
        <coordinates>{wgs84_lng},{wgs84_lat},0</coordinates>
      </Point>
    </Placemark>
'''

    kml_content += '''  </Document>
</kml>'''

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(kml_content)

    print(f"KML文件已生成: {output_file}")
    print(f"\n坐标转换结果:")
    for loc in locations:
        name = loc.get("name", "未命名地点")
        gcj_lng = loc.get("gcj_lng")
        gcj_lat = loc.get("gcj_lat")
        if gcj_lng is not None and gcj_lat is not None:
            wgs84_lng, wgs84_lat = gcj02_to_wgs84(gcj_lng, gcj_lat)
            print(f"  {name}: GCJ-02({gcj_lng},{gcj_lat}) -> WGS-84({wgs84_lng:.6f},{wgs84_lat:.6f})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GCJ-02坐标转WGS-84并生成KML文件")
    parser.add_argument("--name", action="append", help="地点名称")
    parser.add_argument("--lng", type=float, action="append", help="GCJ-02经度")
    parser.add_argument("--lat", type=float, action="append", help="GCJ-02纬度")
    parser.add_argument("--address", action="append", help="地址描述")
    parser.add_argument("--output", default="locations.kml", help="输出KML文件名")
    parser.add_argument("--map-name", default="地图名称", help="地图名称")
    parser.add_argument("--description", default="描述信息", help="地图描述")

    args = parser.parse_args()

    if not args.name or not args.lng or not args.lat:
        print("错误: 请至少提供一个地点的 --name, --lng, --lat 参数")
        parser.print_help()
        sys.exit(1)

    if len(args.name) != len(args.lng) or len(args.name) != len(args.lat):
        print("错误: --name, --lng, --lat 的数量必须一致")
        sys.exit(1)

    addresses = args.address if args.address else [""] * len(args.name)
    # 如果地址数量少于地点数量，用空字符串补齐
    while len(addresses) < len(args.name):
        addresses.append("")

    locations = []
    for i in range(len(args.name)):
        locations.append({
            "name": args.name[i],
            "gcj_lng": args.lng[i],
            "gcj_lat": args.lat[i],
            "address": addresses[i]
        })

    generate_kml(locations, args.map_name, args.description, args.output)
