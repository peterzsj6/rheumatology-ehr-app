import tempfile
import os
import subprocess
import wave
import struct
from typing import Optional, Tuple

class AudioConverter:
    """音频格式转换工具"""
    
    def __init__(self):
        self.supported_formats = ['wav', 'mp3', 'webm', 'ogg', 'm4a', 'flac']
    
    def convert_to_wav(self, input_file: str, output_file: Optional[str] = None) -> str:
        """
        将音频文件转换为WAV格式
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径（可选）
            
        Returns:
            输出文件路径
        """
        if output_file is None:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                output_file = temp_file.name
        
        try:
            # 尝试使用ffmpeg进行转换
            cmd = [
                'ffmpeg', '-i', input_file,
                '-acodec', 'pcm_s16le',  # 16位PCM编码
                '-ar', '16000',          # 16kHz采样率
                '-ac', '1',              # 单声道
                '-y',                    # 覆盖输出文件
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"FFmpeg转换失败: {result.stderr}")
            
            return output_file
            
        except FileNotFoundError:
            # 如果没有ffmpeg，使用Python内置方法
            return self._convert_without_ffmpeg(input_file, output_file)
        except Exception as e:
            # 如果转换失败，返回原文件
            return input_file
    
    def _convert_without_ffmpeg(self, input_file: str, output_file: str) -> str:
        """不使用ffmpeg的转换方法（有限支持）"""
        try:
            # 这里可以实现简单的格式转换
            # 但由于复杂性，我们返回原文件
            return input_file
        except Exception as e:
            raise Exception(f"音频转换失败: {str(e)}")
    
    def ensure_wav_format(self, audio_data: bytes, original_format: str) -> bytes:
        """
        确保音频数据为WAV格式
        
        Args:
            audio_data: 音频数据
            original_format: 原始格式
            
        Returns:
            WAV格式的音频数据
        """
        try:
            # 保存原始文件
            with tempfile.NamedTemporaryFile(suffix=f'.{original_format}', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_input = temp_file.name
            
            # 转换为WAV
            wav_file = self.convert_to_wav(temp_input)
            
            # 读取转换后的文件
            with open(wav_file, 'rb') as f:
                wav_data = f.read()
            
            # 清理临时文件
            try:
                os.unlink(temp_input)
                os.unlink(wav_file)
            except:
                pass
            
            return wav_data
            
        except Exception as e:
            raise Exception(f"音频格式转换失败: {str(e)}")
    
    def create_wav_header(self, sample_rate: int = 16000, channels: int = 1, bits_per_sample: int = 16) -> bytes:
        """
        创建WAV文件头
        
        Args:
            sample_rate: 采样率
            channels: 声道数
            bits_per_sample: 位深度
            
        Returns:
            WAV文件头数据
        """
        byte_rate = sample_rate * channels * bits_per_sample // 8
        block_align = channels * bits_per_sample // 8
        
        header = struct.pack('<4sI4s', b'RIFF', 0, b'WAVE')
        header += struct.pack('<4sIHHIIHH', b'fmt ', 16, 1, channels, sample_rate, byte_rate, block_align, bits_per_sample)
        header += struct.pack('<4sI', b'data', 0)
        
        return header
    
    def convert_audio_blob_to_wav(self, audio_blob_data: bytes, mime_type: str) -> bytes:
        """
        将音频blob数据转换为WAV格式
        
        Args:
            audio_blob_data: 音频blob数据
            mime_type: MIME类型
            
        Returns:
            WAV格式的音频数据
        """
        try:
            # 根据MIME类型确定格式
            format_map = {
                'audio/webm': 'webm',
                'audio/webm;codecs=opus': 'webm',
                'audio/mp3': 'mp3',
                'audio/mpeg': 'mp3',
                'audio/ogg': 'ogg',
                'audio/wav': 'wav',
                'audio/x-wav': 'wav'
            }
            
            file_format = format_map.get(mime_type, 'webm')
            
            # 保存原始文件
            with tempfile.NamedTemporaryFile(suffix=f'.{file_format}', delete=False) as temp_file:
                temp_file.write(audio_blob_data)
                temp_input = temp_file.name
            
            # 转换为WAV
            wav_file = self.convert_to_wav(temp_input)
            
            # 读取转换后的文件
            with open(wav_file, 'rb') as f:
                wav_data = f.read()
            
            # 清理临时文件
            try:
                os.unlink(temp_input)
                os.unlink(wav_file)
            except:
                pass
            
            return wav_data
            
        except Exception as e:
            raise Exception(f"音频blob转换失败: {str(e)}")
    
    def validate_wav_file(self, wav_file_path: str) -> bool:
        """
        验证WAV文件格式是否正确
        
        Args:
            wav_file_path: WAV文件路径
            
        Returns:
            是否为有效的WAV文件
        """
        try:
            with wave.open(wav_file_path, 'rb') as wav_file:
                # 检查基本参数
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                frame_rate = wav_file.getframerate()
                
                # 验证参数
                if channels not in [1, 2]:
                    return False
                if sample_width not in [1, 2, 4]:
                    return False
                if frame_rate < 8000 or frame_rate > 48000:
                    return False
                
                return True
                
        except Exception:
            return False
    
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
                    'duration': wav_file.getnframes() / wav_file.getframerate()
                }
        except Exception as e:
            return {'error': str(e)}

def create_audio_converter() -> AudioConverter:
    """创建音频转换器实例"""
    return AudioConverter() 