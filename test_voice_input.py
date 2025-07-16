#!/usr/bin/env python3
"""
语音输入功能测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    try:
        import streamlit as st
        print("✅ Streamlit导入成功")
        
        import speech_recognition as sr
        print("✅ SpeechRecognition导入成功")
        
        from speech_recognition_service import create_speech_recognition_service
        print("✅ 语音识别服务导入成功")
        
        from voice_input_component import voice_input_section
        print("✅ 语音输入组件导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_speech_service():
    """测试语音识别服务"""
    try:
        from speech_recognition_service import create_speech_recognition_service
        
        # 创建语音识别服务
        service = create_speech_recognition_service(service_type="google")
        print("✅ 语音识别服务创建成功")
        
        # 测试支持的语言
        languages = service.get_supported_languages()
        print(f"✅ 支持的语言: {list(languages.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ 语音识别服务测试失败: {e}")
        return False

def test_main_app():
    """测试主应用程序"""
    try:
        # 模拟Streamlit环境
        import streamlit as st
        
        # 测试提示词类
        from rheumatology_ehr_app import RheumatologyPrompts
        prompts = RheumatologyPrompts()
        print("✅ 提示词类创建成功")
        
        # 测试API配置函数（忽略secrets警告）
        try:
            from rheumatology_ehr_app import get_api_config
            api_key, base_url = get_api_config()
            print(f"✅ API配置获取成功: base_url={base_url}")
        except Exception as e:
            print(f"⚠️ API配置测试跳过（需要secrets配置）: {e}")
        
        return True
    except Exception as e:
        print(f"❌ 主应用程序测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("语音输入功能测试")
    print("=" * 50)
    
    # 测试模块导入
    print("\n1. 测试模块导入...")
    if not test_imports():
        print("❌ 模块导入测试失败")
        return
    
    # 测试语音识别服务
    print("\n2. 测试语音识别服务...")
    if not test_speech_service():
        print("❌ 语音识别服务测试失败")
        return
    
    # 测试主应用程序
    print("\n3. 测试主应用程序...")
    if not test_main_app():
        print("❌ 主应用程序测试失败")
        return
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！")
    print("语音输入功能已成功集成到系统中。")
    print("=" * 50)
    
    print("\n使用说明:")
    print("1. 运行 'streamlit run rheumatology_ehr_app.py' 启动应用")
    print("2. 在浏览器中访问应用")
    print("3. 使用语音输入功能录制问诊记录")
    print("4. 查看生成的电子病历")

if __name__ == "__main__":
    main() 