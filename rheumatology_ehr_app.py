import streamlit as st
import asyncio
import openai
from typing import Dict, Any
import json
from datetime import datetime
import os
import speech_recognition as sr
import tempfile
import wave
import threading
import time
from voice_input_component import voice_input_section
from enhanced_voice_input import enhanced_voice_input_section

# 页面配置
st.set_page_config(
    page_title="风湿免疫科电子病历生成系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .medical-record-table {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .record-section {
        margin-bottom: 1.5rem;
        padding: 1rem;
        background-color: white;
        border-radius: 5px;
        border-left: 4px solid #007bff;
    }
    .record-title {
        font-weight: bold;
        color: #007bff;
        margin-bottom: 0.5rem;
    }
    .record-content {
        color: #333;
        line-height: 1.6;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.2rem;
        background-color: #007bff;
        border-color: #007bff;
    }
    .stButton > button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

class RheumatologyPrompts:
    def __init__(self):
        self.system_prompt = """
        你是一位经验丰富的风湿免疫科专家，专门负责生成风湿免疫科电子病历。
        
        风湿免疫科重点关注：
        1. 关节症状：疼痛、肿胀、晨僵、活动受限、关节畸形
        2. 系统性症状：发热、疲劳、体重下降、皮疹、光敏感
        3. 器官受累：肺间质病变、心包炎、肾炎、神经系统病变
        4. 实验室检查：自身抗体（ANA、RF、抗CCP等）、炎症指标（ESR、CRP）、影像学检查
        
        常见风湿免疫疾病：
        - 类风湿关节炎：对称性多关节炎，晨僵>1小时，RF/抗CCP阳性
        - 系统性红斑狼疮：多系统受累，ANA阳性，光敏感，蝶形红斑
        - 干燥综合征：口干、眼干，抗SSA/SSB阳性
        - 强直性脊柱炎：腰背痛，HLA-B27阳性，骶髂关节炎
        - 系统性硬化症：皮肤硬化，雷诺现象，抗Scl-70阳性
        - 血管炎：多系统血管炎，ANCA阳性
        
        诊断要求：
        1. 基于症状、体征和实验室检查综合分析
        2. 考虑疾病活动度和严重程度
        3. 评估器官受累情况
        4. 排除其他可能的诊断
        
        治疗原则：
        1. 个体化治疗：根据疾病活动度、严重程度和器官受累情况
        2. 早期干预：防止关节破坏和器官损害
        3. 达标治疗：定期评估治疗效果，调整治疗方案
        4. 多学科协作：必要时请相关科室会诊
        5. 患者教育：提高治疗依从性，改善预后
        
        请严格按照风湿免疫科病历格式生成，包括：
        - 主诉（关节症状、系统性症状）
        - 现病史（症状演变、治疗经过）
        - 既往史（其他风湿病、用药史）
        - 体格检查（关节检查、皮肤黏膜、心肺等）
        - 辅助检查（实验室、影像学）
        - 诊断（详细分析诊断方向、鉴别诊断、严重程度评估）
        - 治疗方案（药物治疗、非药物治疗、监测方案、随访计划）
        """
    
    def get_analysis_prompt(self, dialogue):
        return f"""
        请详细分析以下风湿免疫科问诊记录，提取关键信息：
        
        问诊记录：{dialogue}
        
        请识别：
        1. 主要症状和体征（关节症状、系统性症状、器官受累表现）
        2. 症状持续时间和发展过程（急性/慢性、进展性/缓解性）
        3. 既往相关病史（风湿病家族史、自身免疫病史、用药史）
        4. 用药情况（既往用药、药物反应、依从性）
        5. 可能的诊断方向（基于症状和体征的初步判断）
        6. 疾病活动度评估（轻度/中度/重度）
        7. 器官受累情况（关节、皮肤、肺、心、肾、神经系统等）
        8. 需要进一步检查的项目（实验室检查、影像学检查）
        9. 治疗难点和风险因素
        10. 预后影响因素
        """
    
    def get_record_generation_prompt(self, analysis_result):
        return f"""
        基于以下分析结果，生成标准的风湿免疫科电子病历：
        
        分析结果：{analysis_result}
        
        请严格按照以下格式生成电子病历，必须包含以下7个部分，如果对话中未提到相关内容，请对应输出"无"：
        
        主诉：
        [根据对话内容提取患者主要症状，如关节疼痛、皮疹等。如未提到则输出"无"]
        
        现病史：
        [根据对话内容描述症状发展过程、持续时间等。如未提到则输出"无"]
        
        既往史：
        [根据对话内容提取既往病史、用药史等。如未提到则输出"无"]
        
        体格检查：
        [根据对话内容描述关节检查、皮肤黏膜、心肺等检查发现。如未提到则输出"无"]
        
        辅助检查：
        [根据对话内容建议实验室检查、影像学检查等。如未提到则输出"无"]
        
        诊断：
        [请详细分析可能的诊断方向，包括：
        1. 初步诊断：基于症状和体征给出最可能的诊断
        2. 鉴别诊断：列出需要排除的其他风湿免疫疾病
        3. 诊断依据：说明支持诊断的关键症状、体征和检查结果
        4. 疾病严重程度评估：轻度/中度/重度
        5. 并发症风险评估：可能出现的并发症
        如未提到则输出"无"]
        
        治疗方案：
        [请制定详细的治疗方案，包括：
        1. 药物治疗：具体药物名称、剂量、用法、疗程
        2. 非药物治疗：物理治疗、康复训练、生活方式调整
        3. 监测方案：需要定期监测的指标和频率
        4. 随访计划：复诊时间和注意事项
        5. 患者教育：饮食、运动、用药注意事项
        6. 预后评估：预期治疗效果和长期预后
        如未提到则输出"无"]
        
        注意：请严格按照上述格式输出，不要添加其他内容，不要输出分析结果，只输出结构化的电子病历。诊断和治疗方案部分请尽可能详细和具体。
        """

# VoiceRecorder class removed - not needed for Streamlit deployment
# Browser handles recording via JavaScript

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def transcribe_audio(self, audio_file_path):
        """将音频文件转换为文字"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language='zh-CN')
                return text
        except sr.UnknownValueError:
            return "无法识别语音内容"
        except sr.RequestError as e:
            return f"语音识别服务错误: {str(e)}"
        except Exception as e:
            return f"语音转换错误: {str(e)}"

class RheumatologyEHRSystem:
    def __init__(self, api_key: str, base_url: str):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.prompts = RheumatologyPrompts()
    
    async def generate_medical_record(self, consultation_dialogue: str) -> Dict[str, Any]:
        """生成风湿免疫科电子病历"""
        
        try:
            # 第一步：分析问诊内容
            analysis_prompt = self.prompts.get_analysis_prompt(consultation_dialogue)
            analysis_response = await self._call_llm(analysis_prompt)
            
            # 第二步：生成结构化病历
            record_prompt = self.prompts.get_record_generation_prompt(analysis_response)
            record_response = await self._call_llm(record_prompt)
            
            # 第三步：解析和格式化结果
            formatted_record = self._parse_and_format_record(record_response)
            
            return {
                "success": True,
                "medical_record": formatted_record,
                "analysis": analysis_response,
                "raw_response": record_response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _call_llm(self, prompt: str) -> str:
        """调用大模型API"""
        response = self.client.chat.completions.create(
            model="deepseek-v3",
            messages=[
                {"role": "system", "content": self.prompts.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    def _parse_and_format_record(self, record_text: str) -> Dict[str, str]:
        """解析和格式化病历内容"""
        sections = {
            "chief_complaint": "",
            "present_illness": "",
            "past_history": "",
            "physical_examination": "",
            "auxiliary_examination": "",
            "diagnosis": "",
            "treatment_plan": ""
        }
        
        # 更智能的文本解析逻辑
        lines = record_text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是新的章节标题（支持多种格式）
            if any(line.startswith(prefix) for prefix in ["主诉：", "主诉", "现病史：", "现病史", "既往史：", "既往史", "体格检查：", "体格检查", "辅助检查：", "辅助检查", "诊断：", "诊断", "治疗方案：", "治疗方案"]):
                # 保存之前章节的内容
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                    current_content = []
                
                # 设置新的章节
                if line.startswith("主诉") or line.startswith("主诉："):
                    current_section = "chief_complaint"
                elif line.startswith("现病史") or line.startswith("现病史："):
                    current_section = "present_illness"
                elif line.startswith("既往史") or line.startswith("既往史："):
                    current_section = "past_history"
                elif line.startswith("体格检查") or line.startswith("体格检查："):
                    current_section = "physical_examination"
                elif line.startswith("辅助检查") or line.startswith("辅助检查："):
                    current_section = "auxiliary_examination"
                elif line.startswith("诊断") or line.startswith("诊断："):
                    current_section = "diagnosis"
                elif line.startswith("治疗方案") or line.startswith("治疗方案："):
                    current_section = "treatment_plan"
            
            # 如果不是章节标题，且当前有活跃章节，则添加内容
            elif current_section and line and not line.startswith("[") and not line.startswith("请") and not line.startswith("注意") and not line.startswith("基于"):
                current_content.append(line)
        
        # 保存最后一个章节的内容
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # 确保所有章节都有内容，如果没有则设置为"无"
        for key in sections:
            if not sections[key].strip():
                sections[key] = "无"
        
        return sections

def get_api_config():
    """获取API配置，优先使用Streamlit Secrets，然后环境变量，最后默认值"""
    # 优先使用Streamlit Secrets（云端部署）
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
        base_url = st.secrets.get("OPENAI_BASE_URL", "https://vip.apiyi.com/v1")
        return api_key, base_url
    
    # 其次使用环境变量（本地开发）
    api_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", "https://vip.apiyi.com/v1")
    
    return api_key, base_url

def main():
    # 主标题
    st.markdown('<h1 class="main-header">🏥 风湿免疫科电子病历生成系统</h1>', unsafe_allow_html=True)
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 系统配置")
        
        # 获取API配置
        default_api_key, default_base_url = get_api_config()
        
        # API配置
        api_key = st.text_input(
            "OpenAI API Key:",
            value=default_api_key,
            type="password",
            help="请输入您的OpenAI API密钥。如果已配置Secrets或环境变量，将自动填充。"
        )
        
        base_url = st.text_input(
            "API Base URL:",
            value=default_base_url,
            help="API基础URL。如果已配置Secrets或环境变量，将自动填充。"
        )
        
        st.markdown("---")
        
        # 示例问诊记录
        st.header("📋 示例问诊记录")
        example_records = {
            "类风湿关节炎": "患者女性，45岁，主诉双手小关节疼痛、肿胀3个月，晨僵明显，持续时间约2小时，伴有乏力、食欲不振。疼痛呈对称性，以近端指间关节和掌指关节为主，活动后疼痛加重。既往无特殊病史，否认家族风湿病史。",
            "系统性红斑狼疮": "患者女性，28岁，主诉面部蝶形红斑2个月，伴有光敏感、关节疼痛、脱发，近期出现发热、乏力、口腔溃疡。关节疼痛以手指、腕关节为主，呈游走性。既往无特殊病史。",
            "干燥综合征": "患者女性，52岁，主诉口干、眼干1年，伴有吞咽困难、关节疼痛，既往有甲状腺功能减退病史。口干严重，需要频繁饮水，眼干伴有异物感。关节疼痛以手指关节为主。",
            "强直性脊柱炎": "患者男性，25岁，主诉腰背痛2年，晨僵明显，活动后症状改善。疼痛以夜间和晨起为重，逐渐向上发展。既往无特殊病史，父亲有类似症状。",
            "系统性硬化症": "患者女性，38岁，主诉手指雷诺现象3年，皮肤硬化1年。手指遇冷变白、变紫，伴有皮肤紧绷感，逐渐累及面部和躯干。既往无特殊病史。"
        }
        
        selected_example = st.selectbox("选择示例:", list(example_records.keys()))
        if st.button("使用示例"):
            st.session_state.example_text = example_records[selected_example]
    
    # 主界面
    st.markdown('<h2 class="section-header">📝 问诊记录输入</h2>', unsafe_allow_html=True)
    
    # 语音输入功能
    st.markdown('<h3 class="section-header">🎤 语音输入功能</h3>', unsafe_allow_html=True)
    
    # 选择语音输入模式
    input_mode = st.radio(
        "选择语音输入模式：",
        ["基础模式", "增强模式（推荐）"],
        help="增强模式支持自动转换和更多音频格式"
    )
    
    if input_mode == "基础模式":
        voice_input_section()
    else:
        enhanced_voice_input_section()
    
    # 显示转换后的文字
    if hasattr(st.session_state, 'transcribed_text'):
        st.markdown("### 转换结果：")
        st.text_area("语音转换文字：", value=st.session_state.transcribed_text, height=100, key="transcribed_text_area")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 使用此文字", key="use_transcribed_text"):
                st.session_state.example_text = st.session_state.transcribed_text
                st.success("已使用转换的文字！")
        with col2:
            if st.button("🔄 重新转换", key="retry_transcription"):
                del st.session_state.transcribed_text
                st.rerun()
    
    st.markdown("---")
    
    # 文本输入区域
    st.markdown('<h3 class="section-header">✍️ 文本输入</h3>', unsafe_allow_html=True)
    
    # 获取示例文本（如果存在）
    default_text = getattr(st.session_state, 'example_text', '')
    
    consultation_text = st.text_area(
        "请输入医生与患者的完整问诊记录:",
        value=default_text,
        height=200,
        placeholder="例如：患者主诉关节疼痛3个月，晨僵明显，伴有皮疹...（请输入完整的问诊对话记录）"
    )
    
    # 生成按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 生成电子病历", type="primary", use_container_width=True):
            if consultation_text.strip():
                if not api_key:
                    st.error("请输入API Key")
                    return
                
                with st.spinner("正在生成风湿免疫科电子病历..."):
                    try:
                        # 创建EHR系统实例
                        ehr_system = RheumatologyEHRSystem(api_key, base_url)
                        result = asyncio.run(ehr_system.generate_medical_record(consultation_text))
                        display_medical_record(result)
                    except Exception as e:
                        st.error(f"生成失败: {str(e)}")
            else:
                st.error("请输入问诊记录")

def display_medical_record(record_data):
    if not record_data.get("success"):
        st.error(f"生成失败: {record_data.get('error')}")
        return
    
    record = record_data["medical_record"]
    
    st.markdown('<div class="success-box">✅ 电子病历生成完成！</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 显示电子病历表格
    st.markdown('<h2 class="section-header">📋 风湿免疫科电子病历</h2>', unsafe_allow_html=True)
    
    # 使用容器显示病历
    with st.container():
        st.markdown('<div class="medical-record-table">', unsafe_allow_html=True)
        
        # 主诉
        if record.get("chief_complaint"):
            st.markdown(f'''
            <div class="record-section">
                <div class="record-title">主诉</div>
                <div class="record-content">{record.get("chief_complaint", "未生成")}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 现病史
        if record.get("present_illness"):
            st.markdown(f'''
            <div class="record-section">
                <div class="record-title">现病史</div>
                <div class="record-content">{record.get("present_illness", "未生成")}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 既往史
        if record.get("past_history"):
            st.markdown(f'''
            <div class="record-section">
                <div class="record-title">既往史</div>
                <div class="record-content">{record.get("past_history", "未生成")}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 体格检查
        if record.get("physical_examination"):
            st.markdown(f'''
            <div class="record-section">
                <div class="record-title">体格检查</div>
                <div class="record-content">{record.get("physical_examination", "未生成")}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 辅助检查
        if record.get("auxiliary_examination"):
            st.markdown(f'''
            <div class="record-section">
                <div class="record-title">辅助检查</div>
                <div class="record-content">{record.get("auxiliary_examination", "未生成")}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 诊断
        if record.get("diagnosis"):
            st.markdown(f'''
            <div class="record-section">
                <div class="record-title">诊断</div>
                <div class="record-content">{record.get("diagnosis", "未生成")}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 治疗方案
        if record.get("treatment_plan"):
            st.markdown(f'''
            <div class="record-section">
                <div class="record-title">治疗方案</div>
                <div class="record-content">{record.get("treatment_plan", "未生成")}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 底部操作按钮
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 导出为Word", use_container_width=True):
            st.info("Word导出功能待实现")
    
    with col2:
        if st.button("📋 复制到剪贴板", use_container_width=True):
            st.info("复制功能待实现")
    
    with col3:
        if st.button("🔄 重新生成", use_container_width=True):
            st.rerun()
    
    # 可展开的详细信息
    with st.expander("🔍 查看详细信息"):
        tab1, tab2, tab3 = st.tabs(["📊 结构化数据", "🔍 分析结果", "📝 原始响应"])
        
        with tab1:
            st.json(record)
        
        with tab2:
            st.write(record_data.get("analysis", "无分析结果"))
        
        with tab3:
            st.text(record_data.get("raw_response", "无原始响应"))

if __name__ == "__main__":
    main() 