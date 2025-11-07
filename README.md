# AI学习项目

这是一个用于AI学习和实践的Python项目，采用Chocolatey + pyenv-win协同管理Python版本。

## 项目结构

```
AI learning/
├── practice/
│   ├── ai_learning_env/          # 虚拟环境目录
│   ├── ai_learning_project.py    # 主项目文件
│   ├── requirements.txt          # 项目依赖包
│   ├── start_project.bat         # Windows启动脚本
│   ├── test_environment.py       # 环境测试脚本
│   ├── 项目版本日志.md           # 版本变更记录
│   └── README.md                 # 项目说明文档
```

## Chocolatey + pyenv-win 协同管理策略

### 工具定位与分工

#### Chocolatey（系统级包管理器）<mcreference link="https://blog.csdn.net/hello_world_qwp/article/details/148337056" index="1">1</mcreference>
- **定位**: Windows系统级软件包管理
- **职责**: 
  - 安装系统级Python（用于全局工具）
  - 管理pyenv-win等开发工具
  - 安装系统依赖（如Git、Visual Studio Build Tools）
- **优势**: 一键自动化安装，版本回滚支持

#### pyenv-win（Python版本管理器）<mcreference link="https://blog.csdn.net/weixin_40625159/article/details/138060491" index="2">2</mcreference>
- **定位**: 项目级Python版本管理
- **职责**:
  - 管理多个Python版本
  - 按项目切换Python版本
  - 创建虚拟环境
- **优势**: 版本隔离，项目专属环境

### 协同管理架构

```
系统层 (Chocolatey)
├── Python 3.11.9 (全局工具使用)
├── pyenv-win (版本管理工具)
└── Git、Build Tools等系统依赖

项目层 (pyenv-win)
├── Python 3.11.9 (项目专用)
├── ai_learning_env (虚拟环境)
└── 项目依赖包 (requirements.txt)
```

## 环境配置详细说明

### 1. Chocolatey环境配置

#### 安装Chocolatey（管理员权限）
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

#### 通过Chocolatey安装系统工具
```powershell
# 安装系统级Python（用于pip等全局工具）
choco install python311 -y

# 安装pyenv-win
choco install pyenv-win -y

# 安装其他开发工具
choco install git -y
choco install vscode -y
```

### 2. pyenv-win环境配置

#### 安装Python版本（项目专用）
```powershell
# 查看可安装的Python版本
pyenv install --list

# 安装项目需要的Python版本
pyenv install 3.11.9

# 设置为全局默认版本
pyenv global 3.11.9
```

#### 创建虚拟环境
```powershell
# 创建项目虚拟环境
python -m venv ai_learning_env

# 激活虚拟环境
.\ai_learning_env\Scripts\activate
```

## 协同管理最佳实践

### 版本冲突避免策略<mcreference link="https://cloud.tencent.cn/developer/information/%E5%A6%82%E4%BD%95%E4%BF%AE%E5%A4%8D%E5%AE%89%E8%A3%85%E5%8C%85%E5%AF%BC%E8%87%B4%E7%9A%84%E7%8E%AF%E5%A2%83%E4%B8%AD%E7%9A%84python%E7%89%88%E6%9C%AC%E5%86%B2%E7%AA%81%EF%BC%9F-album" index="3">3</mcreference>

#### 1. 环境隔离原则
- **系统Python**: 仅用于安装pip、virtualenv等全局工具
- **项目Python**: 通过pyenv-win管理，每个项目独立版本
- **虚拟环境**: 在项目Python基础上创建，隔离依赖包

#### 2. 路径优先级管理
```
PATH环境变量优先级:
1. 虚拟环境路径 (最高优先级)
2. pyenv-win管理的Python路径
3. Chocolatey安装的系统Python路径 (最低优先级)
```

#### 3. 版本检查命令
```powershell
# 检查当前激活的Python路径
where python

# 检查Python版本
python --version

# 检查pip路径
where pip
```

### 日常使用流程

#### 项目开发启动流程
1. **系统准备**: 确保Chocolatey环境正常
2. **版本切换**: 使用pyenv切换项目Python版本
3. **环境激活**: 激活项目虚拟环境
4. **依赖安装**: 安装requirements.txt中的包
5. **项目运行**: 执行项目代码

#### 快速启动脚本（start_project.bat）
```batch
@echo off
echo 启动AI学习项目...

REM 检查虚拟环境是否存在
if not exist "ai_learning_env" (
    echo 创建虚拟环境...
    python -m venv ai_learning_env
)

REM 激活虚拟环境
call ai_learning_env\Scripts\activate.bat

REM 检查依赖包
python -c "import numpy, pandas, matplotlib, seaborn, sklearn, scipy" 2>nul
if errorlevel 1 (
    echo 安装依赖包...
    pip install -r requirements.txt
)

REM 运行项目
echo 运行AI学习项目...
python ai_learning_project.py

pause
```

## 故障排除与注意事项

### 常见问题解决

#### 1. 版本冲突检测
```powershell
# 检查所有Python安装路径
Get-Command python -All | Format-Table Path, Version

# 检查环境变量优先级
echo $env:PATH
```

#### 2. 虚拟环境问题
- **问题**: 虚拟环境无法激活
- **解决**: 重新创建虚拟环境或检查路径权限

#### 3. 依赖包冲突<mcreference link="https://blog.csdn.net/cda2024/article/details/142765422" index="4">4</mcreference>
- **问题**: 包版本不兼容
- **解决**: 使用虚拟环境隔离，或使用pip freeze生成精确版本

### 重要注意事项

1. **管理员权限**: Chocolatey安装需要管理员权限
2. **环境变量**: 安装后需要重启终端或重新加载环境变量
3. **版本锁定**: 生产环境应锁定Python和依赖包版本
4. **备份策略**: 定期备份虚拟环境和requirements.txt
5. **测试验证**: 使用test_environment.py验证环境配置

## 扩展配置

### 开发工具集成

#### VS Code配置 (.vscode/settings.json)
```json
{
    "python.defaultInterpreterPath": "./ai_learning_env/Scripts/python.exe",
    "python.terminal.activateEnvironment": true
}
```

#### PyCharm配置
- 设置项目解释器为虚拟环境中的Python
- 启用虚拟环境终端

### 持续集成配置

#### GitHub Actions示例
```yaml
name: AI Learning Project CI

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python test_environment.py
```

## 项目功能

### 基础数据分析
- 数据加载和预处理
- 统计描述分析
- 数据可视化

### 机器学习示例
- 线性回归模型（使用加利福尼亚房价数据集）
- 模型评估指标
- 预测结果分析

### 数据可视化
- 分布直方图
- 散点图
- 相关性热力图

## GitHub版本控制配置

### 访问令牌信息

本项目使用GitHub进行版本控制，以下是项目访问令牌信息：

**令牌类型**: Fine-grained Personal Access Token  
**令牌用途**: 用于推送代码到GitHub仓库  
**权限范围**: 仅限当前项目仓库 (`Depression-patient/practice`)

**访问令牌**:  
```
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
```

### 令牌使用说明

#### 1. 配置Git认证
```bash
# 配置Git记住凭据
git config --global credential.helper store

# 推送代码到GitHub（首次需要输入认证信息）
git push -u origin main
```

#### 2. 认证信息输入
当Git提示输入认证信息时：
- **Username**: `Depression-patient`
- **Password**: 使用上面的访问令牌（不是GitHub登录密码）

#### 3. 令牌权限
- **Repository permissions**: 
  - Contents: Read and write
  - Metadata: Read-only
- **有效期**: 根据创建时设置（建议定期更新）

### 安全注意事项

⚠️ **重要安全提醒**:
- 此令牌仅用于当前项目，不要在其他项目中使用
- 令牌具有写权限，请妥善保管
- 如果令牌泄露，请立即在GitHub上撤销
- 定期更新令牌以提高安全性

### 令牌管理

如需修改令牌权限或查看状态：
1. 登录GitHub → Settings → Developer settings → Fine-grained tokens
2. 找到对应令牌进行管理

## 技术支持

如有问题，请参考：
- [Python官方文档](https://docs.python.org/3/)
- [scikit-learn文档](https://scikit-learn.org/stable/)
- [pandas文档](https://pandas.pydata.org/docs/)
- [Chocolatey文档](https://docs.chocolatey.org/)
- [pyenv-win文档](https://github.com/pyenv-win/pyenv-win)

---

**最后更新**: 2025-10-30  
**当前版本**: 1.0.2  
**维护状态**: 活跃维护中