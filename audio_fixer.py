#!/usr/bin/env python3
"""
音频格式修复工具
专门处理Google Speech Recognition兼容性问题
"""

import tempfile
import os
import subprocess
import wave
import struct
from typing import Optional, Tuple

class AudioFixer:
    """音频格式修复工具"""
    
    def __init__(self):
        self.supported_formats = ['wav', 'mp3', 'webm', 'ogg', 'm4a', 'flac']
    
    def fix_audio_for_google_speech(self, input_file: str) -> str:
        """
        修复音频文件以兼容Google Speech Recognition
        
        Args:
            input_file: 输入文件路径
            
        Returns:
            修复后的文件路径
        """
        try:
            # 创建临时输出文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                output_file = temp_file.name
            
            # 使用ffmpeg进行精确转换
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-acodec', 'pcm_s16le',    # 16位PCM编码
                '-ar', '16000',            # 16kHz采样率
                '-ac', '1',                # 单声道
                '-f', 'wav',               # 强制WAV格式
                '-y',                      # 覆盖输出文件
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                # 如果失败，尝试不同的参数
                return self._try_alternative_conversion(input_file, output_file)
            
            # 验证生成的WAV文件
            if not self._validate_wav_for_google(output_file):
                return self._try_alternative_conversion(input_file, output_file)
            
            return output_file
            
        except Exception as e:
            raise Exception(f"音频修复失败: {str(e)}")
    
    def _try_alternative_conversion(self, input_file: str, output_file: str) -> str:
        """尝试替代转换方法"""
        try:
            # 方法1：使用不同的编码参数
            cmd1 = [
                'ffmpeg',
                '-i', input_file,
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                '-ac', '1',
                '-y',
                output_file
            ]
            
            result = subprocess.run(cmd1, capture_output=True, text=True)
            
            if result.returncode == 0 and self._validate_wav_for_google(output_file):
                return output_file
            
            # 方法2：使用更高的采样率
            cmd2 = [
                'ffmpeg',
                '-i', input_file,
                '-acodec', 'pcm_s16le',
                '-ar', '44100',
                '-ac', '1',
                '-y',
                output_file
            ]
            
            result = subprocess.run(cmd2, capture_output=True, text=True)
            
            if result.returncode == 0 and self._validate_wav_for_google(output_file):
                return output_file
            
            # 方法3：使用不同的输出格式
            cmd3 = [
                'ffmpeg',
                '-i', input_file,
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                '-ac', '1',
                '-f', 'wav',
                '-y',
                output_file
            ]
            
            result = subprocess.run(cmd3, capture_output=True, text=True)
            
            if result.returncode == 0:
                return output_file
            
            raise Exception("所有转换方法都失败了")
            
        except Exception as e:
            raise Exception(f"替代转换失败: {str(e)}")
    
    def _validate_wav_for_google(self, wav_file_path: str) -> bool:
        """
        验证WAV文件是否兼容Google Speech Recognition
        
        Args:
            wav_file_path: WAV文件路径
            
        Returns:
            是否兼容
        """
        try:
            with wave.open(wav_file_path, 'rb') as wav_file:
                # 检查基本参数
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                frame_rate = wav_file.getframerate()
                frames = wav_file.getnframes()
                
                # Google Speech Recognition要求
                if channels != 1:  # 必须是单声道
                    return False
                if sample_width != 2:  # 必须是16位
                    return False
                if frame_rate not in [8000, 16000, 44100, 48000]:  # 支持的采样率
                    return False
                if frames == 0:  # 不能为空
                    return False
                
                return True
                
        except Exception:
            return False
    
    def create_compatible_wav(self, audio_data: bytes, original_format: str) -> bytes:
        """
        创建Google Speech Recognition兼容的WAV数据
        
        Args:
            audio_data: 音频数据
            original_format: 原始格式
            
        Returns:
            兼容的WAV数据
        """
        try:
            # 保存原始文件
            with tempfile.NamedTemporaryFile(suffix=f'.{original_format}', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_input = temp_file.name
            
            # 修复音频
            fixed_file = self.fix_audio_for_google_speech(temp_input)
            
            # 读取修复后的文件
            with open(fixed_file, 'rb') as f:
                wav_data = f.read()
            
            # 清理临时文件
            try:
                os.unlink(temp_input)
                os.unlink(fixed_file)
            except:
                pass
            
            return wav_data
            
        except Exception as e:
            raise Exception(f"创建兼容WAV失败: {str(e)}")
    
    def get_audio_info(self, audio_file_path: str) -> dict:
        """
        获取音频文件信息
        
        Args:
            audio_file_path: 音频文件路径
            
        Returns:
            音频信息字典
        """
        try:
            with wave.open(audio_file_path, 'rb') as wav_file:
                return {
                    'channels': wav_file.getnchannels(),
                    'sample_width': wav_file.getsampwidth(),
                    'frame_rate': wav_file.getframerate(),
                    'frames': wav_file.getnframes(),
                    'duration': wav_file.getnframes() / wav_file.getframerate(),
                    'compatible': self._validate_wav_for_google(audio_file_path)
                }
        except Exception as e:
            return {
                'error': str(e),
                'compatible': False
            }
    
    def check_ffmpeg_availability(self) -> bool:
        """检查ffmpeg是否可用"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

def create_audio_fixer() -> AudioFixer:
    """创建音频修复器实例"""
    return AudioFixer() 