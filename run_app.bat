@echo off
echo 启动风湿免疫科电子病历生成系统...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo 安装依赖包...
    pip install -r requirements.txt
)

REM 启动应用
echo 启动应用...
echo 应用将在浏览器中打开，地址：http://localhost:8501
echo 按 Ctrl+C 停止应用
echo.
streamlit run rheumatology_ehr_app.py --server.port 8501

pause 