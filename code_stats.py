#!/usr/bin/env python3
"""
代码统计脚本
统计项目代码行数和文件分布
"""

import os
import glob
from pathlib import Path

def count_lines_in_file(file_path):
    """统计单个文件的行数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0

def get_file_stats():
    """获取文件统计信息"""
    stats = {
        'python_files': [],
        'markdown_files': [],
        'config_files': [],
        'total_lines': 0,
        'total_files': 0
    }
    
    # 获取所有文件
    files = []
    for pattern in ['*.py', '*.md', '*.txt', '*.json', '*.yml', '*.yaml']:
        files.extend(glob.glob(pattern))
    
    # 排除缓存文件
    files = [f for f in files if '__pycache__' not in f and '.pyc' not in f]
    
    for file_path in files:
        lines = count_lines_in_file(file_path)
        if lines > 0:
            if file_path.endswith('.py'):
                stats['python_files'].append((file_path, lines))
            elif file_path.endswith('.md'):
                stats['markdown_files'].append((file_path, lines))
            else:
                stats['config_files'].append((file_path, lines))
            
            stats['total_lines'] += lines
            stats['total_files'] += 1
    
    return stats

def print_stats():
    """打印统计信息"""
    stats = get_file_stats()
    
    print("📊 项目代码统计")
    print("=" * 50)
    
    # Python文件统计
    print("\n🐍 Python文件 ({})".format(len(stats['python_files'])))
    print("-" * 30)
    python_lines = 0
    for file_path, lines in sorted(stats['python_files'], key=lambda x: x[1], reverse=True):
        print(f"{lines:4d} 行  {file_path}")
        python_lines += lines
    
    # Markdown文件统计
    print("\n📝 Markdown文件 ({})".format(len(stats['markdown_files'])))
    print("-" * 30)
    md_lines = 0
    for file_path, lines in sorted(stats['markdown_files'], key=lambda x: x[1], reverse=True):
        print(f"{lines:4d} 行  {file_path}")
        md_lines += lines
    
    # 配置文件统计
    if stats['config_files']:
        print("\n⚙️ 配置文件 ({})".format(len(stats['config_files'])))
        print("-" * 30)
        config_lines = 0
        for file_path, lines in sorted(stats['config_files'], key=lambda x: x[1], reverse=True):
            print(f"{lines:4d} 行  {file_path}")
            config_lines += lines
    
    # 总计
    print("\n📈 总计")
    print("-" * 30)
    print(f"文件总数: {stats['total_files']}")
    print(f"代码总行数: {stats['total_lines']:,}")
    print(f"Python代码: {python_lines:,} 行 ({python_lines/stats['total_lines']*100:.1f}%)")
    print(f"文档行数: {md_lines:,} 行 ({md_lines/stats['total_lines']*100:.1f}%)")
    if stats['config_files']:
        print(f"配置行数: {config_lines:,} 行 ({config_lines/stats['total_lines']*100:.1f}%)")

def analyze_project_structure():
    """分析项目结构"""
    print("\n🏗️ 项目结构分析")
    print("=" * 50)
    
    # 主要功能模块
    main_modules = [
        'rheumatology_ehr_app.py',
        'word_exporter.py',
        'audio_converter.py',
        'audio_fixer.py',
        'streamlit_speech_service.py'
    ]
    
    # 语音输入模块
    voice_modules = [
        'voice_input_component.py',
        'simple_voice_input.py',
        'auto_voice_input.py',
        'enhanced_voice_input.py'
    ]
    
    # 测试模块
    test_modules = [f for f in glob.glob('test_*.py')]
    
    # 文档模块
    doc_modules = [f for f in glob.glob('*.md')]
    
    print(f"主要功能模块: {len(main_modules)} 个")
    print(f"语音输入模块: {len(voice_modules)} 个")
    print(f"测试模块: {len(test_modules)} 个")
    print(f"文档模块: {len(doc_modules)} 个")
    
    print("\n📋 核心功能模块:")
    for module in main_modules:
        if os.path.exists(module):
            lines = count_lines_in_file(module)
            print(f"  • {module} ({lines:,} 行)")
    
    print("\n🎤 语音输入模块:")
    for module in voice_modules:
        if os.path.exists(module):
            lines = count_lines_in_file(module)
            print(f"  • {module} ({lines:,} 行)")

if __name__ == "__main__":
    print_stats()
    analyze_project_structure() 