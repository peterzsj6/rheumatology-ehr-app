import PyInstaller.__main__
import os

# 获取当前目录
current_dir = os.getcwd()

# PyInstaller参数
args = [
    'rheumatology_ehr_app.py',  # 主文件
    '--onefile',  # 打包成单个文件
    '--windowed',  # 无控制台窗口
    '--name=RheumatologyEHRApp',  # 可执行文件名称
    '--add-data=requirements.txt;.',  # 包含requirements.txt
    '--hidden-import=streamlit',
    '--hidden-import=openai',
    '--hidden-import=asyncio',
    '--hidden-import=typing',
    '--hidden-import=json',
    '--hidden-import=datetime',
]

# 运行PyInstaller
PyInstaller.__main__.run(args)

print("打包完成！可执行文件在 dist/ 目录中") 