#!/usr/bin/env python3
"""
Word导出处理器
专门处理Word文档导出，避免页面重新加载问题
"""

import streamlit as st
from datetime import datetime
from word_exporter import create_word_exporter
import pyperclip

class WordExportHandler:
    """Word导出处理器"""
    
    def __init__(self):
        self.word_exporter = create_word_exporter()
    
    def handle_word_export(self, record_data: dict):
        """处理Word导出"""
        try:
            # 生成Word文档
            doc_bytes = self.word_exporter.export_to_bytes(record_data)
            
            # 生成文件名
            filename = f"风湿免疫科电子病历_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            
            # 创建下载按钮
            st.download_button(
                label="📥 下载Word文档",
                data=doc_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key=f"word_download_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            return True, "Word文档已生成，请点击下载按钮保存文件！"
            
        except Exception as e:
            return False, f"Word导出失败: {str(e)}"
    
    def handle_copy_to_clipboard(self, record_data: dict):
        """处理复制到剪贴板"""
        try:
            # 创建病历文本
            record_text = f"""风湿免疫科电子病历

主诉：{record_data.get('chief_complaint', '无')}

现病史：{record_data.get('present_illness', '无')}

既往史：{record_data.get('past_history', '无')}

体格检查：{record_data.get('physical_examination', '无')}

辅助检查：{record_data.get('auxiliary_examination', '无')}

诊断：{record_data.get('diagnosis', '无')}

治疗方案：{record_data.get('treatment_plan', '无')}

生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"""
            
            # 复制到剪贴板
            pyperclip.copy(record_text)
            return True, "病历内容已复制到剪贴板！"
            
        except ImportError:
            return False, "复制功能需要安装pyperclip库：pip install pyperclip"
        except Exception as e:
            return False, f"复制失败: {str(e)}"

def create_word_export_handler() -> WordExportHandler:
    """创建Word导出处理器实例"""
    return WordExportHandler() 