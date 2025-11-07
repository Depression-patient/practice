@echo off
echo ================================
echo    AI学习项目启动脚本
echo ================================
echo.

REM 检查虚拟环境是否存在
if not exist "ai_learning_env" (
    echo 错误: 虚拟环境不存在，请先创建虚拟环境
    echo 运行: python -m venv ai_learning_env
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 正在激活虚拟环境...
call ai_learning_env\Scripts\activate

REM 检查Python版本
echo.
echo 当前Python版本:
python --version

REM 检查依赖包
echo.
echo 检查依赖包安装状态...
python -c "import numpy, pandas, matplotlib, seaborn, sklearn, scipy; print('✓ 所有依赖包已正确安装')" 2>nul
if errorlevel 1 (
    echo 警告: 部分依赖包未安装
    echo 正在安装依赖包...
    pip install -r requirements.txt
)

echo.
echo ================================
echo   项目环境准备完成！
echo ================================
echo.
echo 可用的命令：
echo   1. python ai_learning_project.py  - 运行主项目
echo   2. python test_environment.py    - 测试环境配置
echo   3. jupyter notebook             - 启动Jupyter笔记本
echo.
echo 输入 'deactivate' 退出虚拟环境
echo.
pause