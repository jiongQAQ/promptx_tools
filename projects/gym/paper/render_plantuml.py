#!/usr/bin/env python3
"""
PlantUML渲染工具 - 无需JAR包的替代方案
使用plantuml-python库来渲染PlantUML图表
"""
import sys
import os
import requests
import base64
import zlib
from pathlib import Path

def encode_plantuml(plantuml_text):
    """将PlantUML文本编码为URL安全的格式"""
    # 压缩文本
    compressed = zlib.compress(plantuml_text.encode('utf-8'), 9)
    # Base64编码
    encoded = base64.b64encode(compressed).decode('ascii')
    # 替换字符使其URL安全
    encoded = encoded.replace('+', '-').replace('/', '_').replace('=', '')
    return encoded

def render_plantuml_online(puml_file, output_file, format='png'):
    """使用PlantUML在线服务渲染图表"""
    try:
        # 读取PlantUML文件
        with open(puml_file, 'r', encoding='utf-8') as f:
            plantuml_text = f.read()

        # 编码PlantUML文本
        encoded = encode_plantuml(plantuml_text)

        # 构建请求URL
        server_url = "http://www.plantuml.com/plantuml"
        url = f"{server_url}/{format}/{encoded}"

        print(f"正在渲染: {puml_file} -> {output_file}")
        print(f"请求URL: {url}")

        # 发送请求
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # 保存文件
        with open(output_file, 'wb') as f:
            f.write(response.content)

        print(f"渲染成功: {output_file}")
        return True

    except Exception as e:
        print(f"渲染失败: {e}")
        return False

def render_local_alternative(puml_file, output_file):
    """本地简单渲染替代方案 - 生成文本描述"""
    try:
        with open(puml_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 生成简单的文本描述文件
        txt_file = output_file.replace('.png', '.txt').replace('.svg', '.txt')
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"PlantUML源码内容:\n")
            f.write("=" * 50 + "\n")
            f.write(content)
            f.write("\n" + "=" * 50 + "\n")
            f.write("注: 图片渲染失败，已生成文本描述。\n")

        print(f"生成文本描述: {txt_file}")
        return True

    except Exception as e:
        print(f"生成文本描述失败: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("用法: python render_plantuml.py <input.puml> <output.png>")
        sys.exit(1)

    puml_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(puml_file):
        print(f"输入文件不存在: {puml_file}")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 尝试在线渲染
    if render_plantuml_online(puml_file, output_file):
        print("使用在线服务渲染成功")
    else:
        print("在线服务失败，使用本地替代方案")
        render_local_alternative(puml_file, output_file)

if __name__ == "__main__":
    main()