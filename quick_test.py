#!/usr/bin/env python3
"""
快速测试脚本 - 验证语音输入核心功能
"""

def test_core_imports():
    """测试核心模块导入"""
    print("🔍 测试核心模块导入...")
    
    try:
        import streamlit as st
        print("✅ streamlit 导入成功")
    except ImportError as e:
        print(f"❌ streamlit 导入失败: {e}")
        return False
    
    try:
        import speech_recognition as sr
        print("✅ speech_recognition 导入成功")
    except ImportError as e:
        print(f"❌ speech_recognition 导入失败: {e}")
        return False
    
    try:
        from streamlit_speech_service import create_streamlit_speech_service
        print("✅ streamlit_speech_service 导入成功")
    except ImportError as e:
        print(f"❌ streamlit_speech_service 导入失败: {e}")
        return False
    
    try:
        from audio_converter import AudioConverter
        print("✅ audio_converter 导入成功")
    except ImportError as e:
        print(f"❌ audio_converter 导入失败: {e}")
        return False
    
    return True

def test_voice_components():
    """测试语音输入组件"""
    print("\n🔍 测试语音输入组件...")
    
    try:
        from voice_input_component import voice_input_section
        print("✅ voice_input_component 导入成功")
    except ImportError as e:
        print(f"❌ voice_input_component 导入失败: {e}")
        return False
    
    try:
        from simple_voice_input import simple_voice_input_section
        print("✅ simple_voice_input 导入成功")
    except ImportError as e:
        print(f"❌ simple_voice_input 导入失败: {e}")
        return False
    
    try:
        from auto_voice_input import auto_voice_input_section
        print("✅ auto_voice_input 导入成功")
    except ImportError as e:
        print(f"❌ auto_voice_input 导入失败: {e}")
        return False
    
    try:
        from enhanced_voice_input import enhanced_voice_input_section
        print("✅ enhanced_voice_input 导入成功")
    except ImportError as e:
        print(f"❌ enhanced_voice_input 导入失败: {e}")
        return False
    
    return True

def test_speech_services():
    """测试语音识别服务"""
    print("\n🔍 测试语音识别服务...")
    
    try:
        from streamlit_speech_service import create_streamlit_speech_service
        
        # 测试Google语音识别服务
        speech_service = create_streamlit_speech_service(service_type="google")
        print("✅ Google语音识别服务创建成功")
        
        # 测试其他服务
        services = ["azure", "baidu", "tencent"]
        for service in services:
            try:
                speech_service = create_streamlit_speech_service(service_type=service)
                print(f"✅ {service}语音识别服务创建成功")
            except Exception as e:
                print(f"⚠️ {service}语音识别服务创建失败: {e}")
        
        return True
    except Exception as e:
        print(f"❌ 语音识别服务测试失败: {e}")
        return False

def test_main_app():
    """测试主应用程序核心功能"""
    print("\n🔍 测试主应用程序核心功能...")
    
    try:
        # 直接导入核心类，不依赖Streamlit环境
        from rheumatology_ehr_app import RheumatologyPrompts, RheumatologyEHRSystem
        
        # 测试提示词系统
        prompts = RheumatologyPrompts()
        print("✅ 提示词系统创建成功")
        
        # 测试提示词生成
        analysis_prompt = prompts.get_analysis_prompt("患者主诉关节疼痛")
        print("✅ 分析提示词生成成功")
        
        record_prompt = prompts.get_record_generation_prompt("分析结果")
        print("✅ 病历生成提示词生成成功")
        
        return True
    except Exception as e:
        print(f"❌ 主应用程序测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始快速测试语音输入组件...\n")
    
    # 测试核心模块导入
    if not test_core_imports():
        print("\n❌ 核心模块导入测试失败")
        return False
    
    # 测试语音输入组件
    if not test_voice_components():
        print("\n❌ 语音输入组件测试失败")
        return False
    
    # 测试语音识别服务
    if not test_speech_services():
        print("\n❌ 语音识别服务测试失败")
        return False
    
    # 测试主应用程序
    if not test_main_app():
        print("\n❌ 主应用程序测试失败")
        return False
    
    print("\n✅ 所有核心功能测试通过！")
    print("\n📝 问题解决方案：")
    print("1. 如果语音转换卡住，请使用'简化模式'或'自动模式'")
    print("2. 简化模式：录音后下载文件，然后上传转换")
    print("3. 自动模式：录音后自动下载，然后上传转换")
    print("4. 如果转换失败，系统会提供示例文字")
    print("5. 确保浏览器允许麦克风访问权限")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 