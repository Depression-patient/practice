#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境测试脚本
用于验证Python环境和依赖包是否正确安装
"""

import sys
import importlib

def check_python_version():
    """检查Python版本"""
    print("=== Python版本检查 ===")
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
def check_package_installation():
    """检查关键包是否安装"""
    print("\n=== 依赖包检查 ===")
    
    packages = [
        'numpy',
        'pandas', 
        'matplotlib',
        'seaborn',
        'sklearn',
        'scipy'
    ]
    
    for package in packages:
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', '未知版本')
            print(f"✓ {package}: {version}")
        except ImportError:
            print(f"✗ {package}: 未安装")

def test_basic_functionality():
    """测试基本功能"""
    print("\n=== 基本功能测试 ===")
    
    try:
        import numpy as np
        # 测试numpy
        arr = np.array([1, 2, 3, 4, 5])
        print(f"✓ NumPy数组创建成功: {arr}")
        
        import pandas as pd
        # 测试pandas
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        print(f"✓ Pandas DataFrame创建成功")
        print(df)
        
        print("✓ 所有基本功能测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始环境测试...\n")
    
    # 检查Python版本
    check_python_version()
    
    # 检查包安装
    check_package_installation()
    
    # 测试基本功能
    success = test_basic_functionality()
    
    print("\n=== 测试结果 ===")
    if success:
        print("🎉 环境配置成功！所有测试通过。")
        print("您可以开始使用AI学习项目了。")
    else:
        print("❌ 环境配置存在问题，请检查依赖包安装。")
    
    return success

if __name__ == "__main__":
    main()