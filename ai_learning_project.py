#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI学习项目主文件
包含常用的AI学习示例代码
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def basic_data_analysis():
    """基础数据分析示例"""
    print("=== 基础数据分析示例 ===")
    
    # 创建示例数据
    data = {
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'target': np.random.randn(100)
    }
    df = pd.DataFrame(data)
    
    print("数据基本信息:")
    print(df.info())
    print("\n数据统计描述:")
    print(df.describe())
    
    return df

def linear_regression_example():
    """线性回归示例"""
    print("\n=== 线性回归示例 ===")
    
    # 加载加利福尼亚房价数据集（替代已移除的Boston数据集）
    california = datasets.fetch_california_housing()
    X = california.data
    y = california.target
    
    print(f"数据集信息: {california.DESCR[:200]}...")
    print(f"特征数量: {X.shape[1]}")
    print(f"样本数量: {X.shape[0]}")
    print(f"目标变量范围: {y.min():.2f} - {y.max():.2f}")
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 创建并训练模型
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 预测
    y_pred = model.predict(X_test)
    
    # 评估模型
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"均方误差 (MSE): {mse:.2f}")
    print(f"R² 分数: {r2:.2f}")
    
    return model, X_test, y_test, y_pred

def data_visualization(california_data):
    """数据可视化示例"""
    print("\n=== 数据可视化示例 ===")
    
    # 设置图形样式
    plt.style.use('seaborn-v0_8')
    
    # 创建子图
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. 房价分布直方图
    axes[0, 0].hist(california_data.target, bins=30, alpha=0.7, color='skyblue')
    axes[0, 0].set_title('加利福尼亚房价分布')
    axes[0, 0].set_xlabel('房价（万美元）')
    axes[0, 0].set_ylabel('频数')
    
    # 2. 房屋年龄分布直方图
    axes[0, 1].hist(california_data.data[:, 1], bins=30, alpha=0.7, color='lightcoral')
    axes[0, 1].set_title('房屋年龄分布')
    axes[0, 1].set_xlabel('房屋年龄')
    axes[0, 1].set_ylabel('频数')
    
    # 3. 房屋年龄与房价关系散点图
    axes[1, 0].scatter(california_data.data[:, 1], california_data.target, alpha=0.6, color='green')
    axes[1, 0].set_title('房屋年龄 vs 房价')
    axes[1, 0].set_xlabel('房屋年龄')
    axes[1, 0].set_ylabel('房价（万美元）')
    
    # 4. 相关性热力图
    feature_names = california_data.feature_names
    df = pd.DataFrame(california_data.data, columns=feature_names)
    df['房价'] = california_data.target
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=axes[1, 1])
    axes[1, 1].set_title('加利福尼亚房价数据集相关性热力图')
    
    plt.tight_layout()
    plt.savefig('california_housing_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("可视化图表已保存为 'california_housing_analysis.png'")

def main():
    """主函数"""
    print("AI学习项目启动...")
    print(f"Python版本: {sys.version}")
    
    # 基础数据分析
    df = basic_data_analysis()
    
    # 线性回归示例
    model, X_test, y_test, y_pred = linear_regression_example()
    
    # 加载加利福尼亚房价数据用于可视化
    california = datasets.fetch_california_housing()
    
    # 数据可视化
    data_visualization(california)
    
    print("\n=== 项目完成 ===")
    print("所有示例代码已成功运行！")

if __name__ == "__main__":
    import sys
    main()