#!/usr/bin/env python3
"""
测试语音输入组件的脚本
"""

import sys
import os

def test_imports():
    """测试所有必要的模块导入"""
    print("🔍 测试模块导入...")
    
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
        from voice_input_component import voice_input_section
        print("✅ voice_input_component 导入成功")
    except ImportError as e:
        print(f"❌ voice_input_component 导入失败: {e}")
        return False
    
    try:
        from enhanced_voice_input import enhanced_voice_input_section
        print("✅ enhanced_voice_input 导入成功")
    except ImportError as e:
        print(f"❌ enhanced_voice_input 导入失败: {e}")
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

def test_speech_service():
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

def test_audio_converter():
    """测试音频转换器"""
    print("\n🔍 测试音频转换器...")
    
    try:
        from audio_converter import AudioConverter
        
        converter = AudioConverter()
        print("✅ 音频转换器创建成功")
        
        # 检查ffmpeg是否可用
        try:
            import subprocess
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ ffmpeg 可用")
            else:
                print("⚠️ ffmpeg 不可用，音频转换功能可能受限")
        except FileNotFoundError:
            print("⚠️ ffmpeg 未安装，音频转换功能可能受限")
        
        return True
    except Exception as e:
        print(f"❌ 音频转换器测试失败: {e}")
        return False

def test_main_app():
    """测试主应用程序"""
    print("\n🔍 测试主应用程序...")
    
    try:
        # 模拟Streamlit环境
        import sys
        sys.modules['streamlit'] = type('MockStreamlit', (), {
            'set_page_config': lambda **kwargs: None,
            'markdown': lambda text, **kwargs: None,
            'sidebar': type('MockSidebar', (), {'header': lambda x: None}),
            'text_input': lambda **kwargs: "test_key",
            'selectbox': lambda **kwargs: "google",
            'button': lambda **kwargs: False,
            'spinner': lambda text: type('MockSpinner', (), {'__enter__': lambda self: None, '__exit__': lambda self, *args: None})(),
            'success': lambda text: None,
            'error': lambda text: None,
            'info': lambda text: None,
            'warning': lambda text: None,
            'columns': lambda n: [type('MockColumn', (), {}) for _ in range(n)],
            'expander': lambda text: type('MockExpander', (), {'__enter__': lambda self: None, '__exit__': lambda self, *args: None})(),
            'tabs': lambda tabs: [type('MockTab', (), {'__enter__': lambda self: None, '__exit__': lambda self, *args: None}) for _ in tabs],
            'json': lambda data: None,
            'write': lambda text: None,
            'text': lambda text: None,
            'container': lambda: type('MockContainer', (), {'__enter__': lambda self: None, '__exit__': lambda self, *args: None})(),
            'rerun': lambda: None,
            'session_state': type('MockSessionState', (), {})(),
            'secrets': type('MockSecrets', (), {})(),
            'file_uploader': lambda **kwargs: None,
            'audio': lambda data, **kwargs: None,
            'radio': lambda **kwargs: "基础模式",
            'text_area': lambda **kwargs: "",
            'components': type('MockComponents', (), {'html': lambda html, **kwargs: None})(),
        })()
        
        # 导入主应用程序
        from rheumatology_ehr_app import RheumatologyEHRSystem, RheumatologyPrompts
        
        # 测试提示词系统
        prompts = RheumatologyPrompts()
        print("✅ 提示词系统创建成功")
        
        # 测试EHR系统
        ehr_system = RheumatologyEHRSystem("test_key", "https://test.api.com")
        print("✅ EHR系统创建成功")
        
        return True
    except Exception as e:
        print(f"❌ 主应用程序测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试语音输入组件...\n")
    
    # 测试模块导入
    if not test_imports():
        print("\n❌ 模块导入测试失败")
        return False
    
    # 测试语音识别服务
    if not test_speech_service():
        print("\n❌ 语音识别服务测试失败")
        return False
    
    # 测试音频转换器
    if not test_audio_converter():
        print("\n❌ 音频转换器测试失败")
        return False
    
    # 测试主应用程序
    if not test_main_app():
        print("\n❌ 主应用程序测试失败")
        return False
    
    print("\n✅ 所有测试通过！语音输入组件应该可以正常工作。")
    print("\n📝 使用说明：")
    print("1. 运行 'streamlit run rheumatology_ehr_app.py' 启动应用")
    print("2. 选择不同的语音输入模式进行测试")
    print("3. 简化模式最稳定，自动模式最便捷")
    print("4. 如果遇到问题，请检查浏览器控制台和Streamlit日志")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 