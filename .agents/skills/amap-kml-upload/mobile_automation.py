# -*- encoding=utf8 -*-
"""
高德地图小程序KML文件上传自动化脚本
使用Airtest框架
"""

__author__ = "Lingma"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import time
import os

# 初始化
auto_setup(__file__, devices=["Android:///"])
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

# KML文件路径（需要先推送到手机）
KML_FILE_PATH = "/sdcard/Download/shanghai_transport_locations.kml"
MAP_NAME = "上海市交通机构位置"


def push_file_to_phone(kml_path):
    """将KML文件推送到手机"""
    local_file = kml_path
    remote_path = "/sdcard/Download/"
    os.system(f"adb push {local_file} {remote_path}")
    print(f"文件已推送到: {remote_path}")


def open_amap_miniprogram():
    """打开高德地图小程序"""
    # 方法1: 如果已安装高德地图APP
    start_app("com.autonavi.minimap")
    sleep(2)
    
    # 方法2: 如果在微信中打开小程序
    # start_app("com.tencent.mm")
    # poco(text="发现").click()
    # poco(text="小程序").click()
    # poco(text="搜索小程序").click()
    # poco(type="EditText").set_text("高德地图小程序")
    # sleep(1)
    # poco(textContains="高德地图").click()
    
    sleep(3)


def login_if_needed():
    """检查并处理登录"""
    try:
        if poco(text="手机号码").exists():
            print("需要登录，请手动完成登录")
            # 这里可以添加自动登录逻辑，但建议手动登录以处理验证码
            wait_for_login()
    except:
        pass


def wait_for_login(timeout=60):
    """等待用户完成登录"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not poco(text="手机号码").exists():
            print("登录完成")
            return True
        sleep(1)
    raise TimeoutError("登录超时")


def create_new_map(map_name):
    """创建新地图"""
    # 点击创建新地图
    poco(text="创建新地图").click()
    sleep(1)
    
    # 输入地图名称
    poco(type="EditText").set_text(map_name)
    sleep(0.5)
    
    # 点击创建
    poco(text="创建").click()
    sleep(3)
    
    print(f"地图 '{map_name}' 创建成功")


def enter_map_editor():
    """进入地图编辑页面"""
    # 等待地图加载
    sleep(3)
    
    # 检查是否已进入编辑页面
    if poco(text="批量导入").exists():
        print("已进入地图编辑页面")
        return True
    
    # 如果没有，尝试点击地图列表中的第一个地图
    try:
        poco(textContains="创建于").click()
        sleep(3)
    except:
        raise Exception("无法进入地图编辑页面")


def upload_kml_file():
    """上传KML文件"""
    # 点击批量导入
    poco(text="批量导入").click()
    sleep(1)
    
    # 选择数据来源为"谷歌地图"（关键步骤！）
    poco(text="高德地图(推荐)").click()
    sleep(0.5)
    poco(text="谷歌地图").click()
    sleep(0.5)
    
    # 点击上传区域
    poco(textContains="点击或拖拽").click()
    sleep(1)
    
    # 在文件选择器中选择KML文件
    # 可能需要导航到Download目录
    try:
        poco(text="Download").click()
        sleep(0.5)
    except:
        pass
    
    # 选择KML文件
    poco(textContains=".kml").click()
    sleep(2)
    
    # 等待上传和解析
    print("正在上传和解析...")
    max_wait = 30
    while max_wait > 0:
        if poco(textContains="成功导入").exists():
            break
        if poco(textContains="不支持").exists():
            raise Exception("文件格式不支持，请确认选择了'谷歌地图'作为数据来源")
        sleep(1)
        max_wait -= 1
    
    # 点击完成
    poco(text="完成").click()
    sleep(1)
    
    print("KML文件上传成功！")


def verify_upload():
    """验证上传结果"""
    sleep(2)
    
    # 检查是否有导入的数据
    if poco(textContains="批量导入").exists() or poco(textContains="(3)").exists():
        print("验证成功：数据已导入")
        return True
    else:
        print("验证失败：未找到导入的数据")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("高德地图KML上传自动化开始")
    print("=" * 50)
    
    try:
        # 1. 推送文件到手机
        push_file_to_phone(KML_FILE_PATH)
        
        # 2. 打开高德地图小程序
        open_amap_miniprogram()
        
        # 3. 检查登录状态
        login_if_needed()
        
        # 4. 创建新地图
        create_new_map(MAP_NAME)
        
        # 5. 进入地图编辑器
        enter_map_editor()
        
        # 6. 上传KML文件
        upload_kml_file()
        
        # 7. 验证上传结果
        verify_upload()
        
        print("=" * 50)
        print("自动化完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"错误: {str(e)}")
        snapshot(msg=f"error_{int(time.time())}")
        raise


if __name__ == "__main__":
    main()
