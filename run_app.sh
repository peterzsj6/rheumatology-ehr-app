#!/bin/bash

echo "启动风湿免疫科电子病历生成系统..."
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python，请先安装Python 3.8+"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖包..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "安装依赖包..."
    pip3 install -r requirements.txt
fi

# 启动应用
echo "启动应用..."
echo "应用将在浏览器中打开，地址：http://localhost:8501"
echo "按 Ctrl+C 停止应用"
echo
streamlit run rheumatology_ehr_app.py --server.port 8501 