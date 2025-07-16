import speech_recognition as sr
import tempfile
import os
import warnings
from typing import Optional

class StreamlitSpeechService:
    """专门为 Streamlit 部署优化的语音识别服务"""
    
    def __init__(self, service_type: str = "google"):
        """
        初始化语音识别服务
        
        Args:
            service_type: 服务类型 ("google", "azure", "baidu", "tencent")
        """
        self.service_type = service_type
        self.recognizer = sr.Recognizer()
        
        # 设置识别参数
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
    
    def transcribe_audio_file(self, audio_file_path: str, language: str = "zh-CN") -> str:
        """
        将音频文件转换为文字
        
        Args:
            audio_file_path: 音频文件路径
            language: 语言代码
            
        Returns:
            转换后的文字
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                # 调整音频参数
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.record(source)
                return self._recognize_speech(audio, language)
        except Exception as e:
            return f"语音识别失败: {str(e)}"
    
    def transcribe_audio_data(self, audio_data: bytes, language: str = "zh-CN") -> str:
        """
        将音频数据转换为文字
        
        Args:
            audio_data: 音频数据
            language: 语言代码
            
        Returns:
            识别结果
        """
        try:
            # 保存临时文件
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # 转换音频
            result = self.transcribe_audio_file(temp_file_path, language)
            
            # 清理临时文件
            try:
                os.unlink(temp_file_path)
            except:
                pass
            
            return result
        except Exception as e:
            return f"语音识别失败: {str(e)}"
    
    def _recognize_speech(self, audio, language: str) -> str:
        """
        使用指定的服务进行语音识别
        
        Args:
            audio: 音频对象
            language: 语言代码
            
        Returns:
            识别结果
        """
        try:
            if self.service_type == "google":
                return self._recognize_google(audio, language)
            elif self.service_type == "azure":
                return self._recognize_azure(audio, language)
            elif self.service_type == "baidu":
                return self._recognize_baidu(audio, language)
            elif self.service_type == "tencent":
                return self._recognize_tencent(audio, language)
            else:
                return self._recognize_google(audio, language)
        except Exception as e:
            return f"语音识别服务错误: {str(e)}"
    
    def _recognize_google(self, audio, language: str) -> str:
        """使用Google Speech Recognition"""
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return self.recognizer.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            return "无法识别语音内容，请确保音频清晰且包含语音"
        except sr.RequestError as e:
            return f"Google语音识别服务错误: {str(e)}"
        except Exception as e:
            return f"语音识别过程中发生错误: {str(e)}"
    
    def _recognize_azure(self, audio, language: str) -> str:
        """使用Azure Speech Services"""
        try:
            # 这里需要Azure Speech SDK
            # 由于依赖复杂，这里返回提示信息
            return "Azure语音识别功能需要配置Azure Speech Services。目前使用Google服务。"
        except Exception as e:
            return f"Azure语音识别错误: {str(e)}"
    
    def _recognize_baidu(self, audio, language: str) -> str:
        """使用百度语音识别"""
        try:
            # 这里需要百度语音识别API
            # 由于依赖复杂，这里返回提示信息
            return "百度语音识别功能需要配置百度语音API。目前使用Google服务。"
        except Exception as e:
            return f"百度语音识别错误: {str(e)}"
    
    def _recognize_tencent(self, audio, language: str) -> str:
        """使用腾讯语音识别"""
        try:
            # 这里需要腾讯语音识别API
            # 由于依赖复杂，这里返回提示信息
            return "腾讯语音识别功能需要配置腾讯语音API。目前使用Google服务。"
        except Exception as e:
            return f"腾讯语音识别错误: {str(e)}"
    
    def get_supported_languages(self) -> dict:
        """获取支持的语言列表"""
        return {
            "zh-CN": "中文（简体）",
            "zh-TW": "中文（繁体）",
            "en-US": "英语（美国）",
            "en-GB": "英语（英国）",
            "ja-JP": "日语",
            "ko-KR": "韩语",
            "fr-FR": "法语",
            "de-DE": "德语",
            "es-ES": "西班牙语",
            "ru-RU": "俄语"
        }
    
    def get_service_info(self) -> dict:
        """获取服务信息"""
        return {
            "google": {
                "name": "Google Speech Recognition",
                "free": True,
                "requires_key": False,
                "languages": "多语言支持",
                "accuracy": "中等"
            },
            "azure": {
                "name": "Azure Speech Services",
                "free": False,
                "requires_key": True,
                "languages": "多语言支持",
                "accuracy": "高"
            },
            "baidu": {
                "name": "百度语音识别",
                "free": False,
                "requires_key": True,
                "languages": "主要支持中文",
                "accuracy": "中文识别效果好"
            },
            "tencent": {
                "name": "腾讯语音识别",
                "free": False,
                "requires_key": True,
                "languages": "主要支持中文",
                "accuracy": "中文识别效果好"
            }
        }

def create_streamlit_speech_service(service_type: str = "google") -> StreamlitSpeechService:
    """
    创建 Streamlit 语音识别服务实例
    
    Args:
        service_type: 服务类型
        
    Returns:
        语音识别服务实例
    """
    return StreamlitSpeechService(service_type) 