#!/usr/bin/env python3
"""
测试音频修复功能
"""

import os
import tempfile
from audio_fixer import create_audio_fixer

def test_audio_fixer():
    """测试音频修复器"""
    print("🔍 测试音频修复器...")
    
    try:
        # 创建音频修复器
        audio_fixer = create_audio_fixer()
        print("✅ 音频修复器创建成功")
        
        # 检查ffmpeg可用性
        if audio_fixer.check_ffmpeg_availability():
            print("✅ ffmpeg 可用")
        else:
            print("⚠️ ffmpeg 不可用，音频修复功能可能受限")
        
        return True
    except Exception as e:
        print(f"❌ 音频修复器测试失败: {e}")
        return False

def test_audio_conversion():
    """测试音频转换功能"""
    print("\n🔍 测试音频转换功能...")
    
    try:
        from audio_converter import create_audio_converter
        
        # 创建音频转换器
        audio_converter = create_audio_converter()
        print("✅ 音频转换器创建成功")
        
        return True
    except Exception as e:
        print(f"❌ 音频转换器测试失败: {e}")
        return False

def test_speech_service():
    """测试语音识别服务"""
    print("\n🔍 测试语音识别服务...")
    
    try:
        from streamlit_speech_service import create_streamlit_speech_service
        
        # 创建语音识别服务
        speech_service = create_streamlit_speech_service(service_type="google")
        print("✅ 语音识别服务创建成功")
        
        return True
    except Exception as e:
        print(f"❌ 语音识别服务测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试音频修复功能...\n")
    
    # 测试音频修复器
    if not test_audio_fixer():
        print("\n❌ 音频修复器测试失败")
        return False
    
    # 测试音频转换器
    if not test_audio_conversion():
        print("\n❌ 音频转换器测试失败")
        return False
    
    # 测试语音识别服务
    if not test_speech_service():
        print("\n❌ 语音识别服务测试失败")
        return False
    
    print("\n✅ 所有音频修复功能测试通过！")
    print("\n📝 解决Google Speech Recognition兼容性问题的方案：")
    print("1. 使用音频修复器自动修复音频格式")
    print("2. 确保音频为16位PCM、16kHz采样率、单声道")
    print("3. 如果修复失败，会尝试其他转换方法")
    print("4. 提供详细的错误信息和解决建议")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 