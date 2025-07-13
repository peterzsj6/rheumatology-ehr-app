import openai
import asyncio
from typing import Dict, Any

class RheumatologyPrompts:
    def __init__(self):
        self.system_prompt = """
        你是一位经验丰富的风湿免疫科专家，专门负责生成风湿免疫科电子病历。
        
        风湿免疫科重点关注：
        1. 关节症状：疼痛、肿胀、晨僵、活动受限
        2. 系统性症状：发热、疲劳、体重下降、皮疹
        3. 器官受累：肺、心、肾、神经系统
        4. 实验室检查：自身抗体、炎症指标、影像学
        
        请严格按照风湿免疫科病历格式生成，包括：
        - 主诉（关节症状、系统性症状）
        - 现病史（症状演变、治疗经过）
        - 既往史（其他风湿病、用药史）
        - 体格检查（关节检查、皮肤黏膜、心肺等）
        - 辅助检查（实验室、影像学）
        - 诊断（初步诊断、鉴别诊断）
        - 治疗方案
        """
    
    def get_analysis_prompt(self, dialogue):
        return f"""
        请分析以下风湿免疫科问诊记录，提取关键信息：
        
        问诊记录：{dialogue}
        
        请识别：
        1. 主要症状和体征
        2. 症状持续时间和发展过程
        3. 既往相关病史
        4. 用药情况
        5. 可能的诊断方向
        """
    
    def get_record_generation_prompt(self, analysis_result):
        return f"""
        基于以下分析结果，生成标准的风湿免疫科电子病历：
        
        分析结果：{analysis_result}
        
        请生成包含以下部分的完整病历：
        1. 主诉
        2. 现病史
        3. 既往史
        4. 体格检查
        5. 辅助检查建议
        6. 诊断
        7. 治疗方案
        """

class RheumatologyEHRAgent:
    def __init__(self):
        self.specialty_knowledge = {
            "diseases": [
                "类风湿关节炎", "系统性红斑狼疮", "干燥综合征", 
                "强直性脊柱炎", "痛风", "血管炎", "皮肌炎"
            ],
            "key_symptoms": [
                "关节疼痛", "晨僵", "皮疹", "光敏感", "口干眼干",
                "雷诺现象", "肌痛", "发热", "体重下降"
            ],
            "lab_tests": [
                "RF", "抗CCP抗体", "ANA", "抗dsDNA抗体", 
                "补体C3/C4", "ESR", "CRP", "肌酸激酶"
            ]
        }
    
    async def generate_rheumatology_record(self, consultation_dialogue):
        """一站式生成风湿免疫科电子病历"""
        
        # 1. 分析问诊内容（识别风湿免疫相关症状和体征）
        analysis = await self._analyze_rheumatology_content(consultation_dialogue)
        
        # 2. 生成结构化病历（结合风湿免疫科特点）
        record = await self._generate_structured_record(analysis)
        
        # 3. 质量检查和优化（风湿免疫科专业标准）
        final_record = await self._quality_check_and_optimize(record)
        
        return final_record
    
    async def _call_llm(self, prompt: str) -> str:
        """调用大模型API"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.prompts.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # 降低随机性，提高一致性
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
        
        # 简单的文本解析逻辑
        lines = record_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 识别章节标题
            if any(keyword in line for keyword in ["主诉", "现病史", "既往史", "体格检查", "辅助检查", "诊断", "治疗"]):
                for key in sections.keys():
                    if any(keyword in line for keyword in ["主诉", "现病史", "既往史", "体格检查", "辅助检查", "诊断", "治疗"]):
                        current_section = key
                        break
            elif current_section:
                sections[current_section] += line + "\n"
        
        return sections


### **Web界面实现**


import streamlit as st
import asyncio

def main():
    st.set_page_config(
        page_title="风湿免疫科电子病历生成系统",
        page_icon="",
        layout="wide"
    )
    
    st.title("🏥 风湿免疫科电子病历生成系统")
    st.markdown("---")
    
    # 输入区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 问诊记录输入")
        consultation_text = st.text_area(
            "请输入医生与患者的问诊记录:",
            height=300,
            placeholder="例如：患者主诉关节疼痛3个月，晨僵明显，伴有皮疹..."
        )
    
    with col2:
        st.subheader("⚙️ 设置")
        model_choice = st.selectbox(
            "选择模型:",
            ["gpt-4", "gpt-3.5-turbo"],
            index=0
        )
        
        temperature = st.slider(
            "创造性 (Temperature):",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1
        )
    
    # 生成按钮
    if st.button("🚀 生成电子病历", type="primary"):
        if consultation_text.strip():
            with st.spinner("正在生成风湿免疫科电子病历..."):
                result = asyncio.run(generate_rheumatology_record(consultation_text))
                display_medical_record(result)
        else:
            st.error("请输入问诊记录")

def display_medical_record(record_data):
    if not record_data.get("success"):
        st.error(f"生成失败: {record_data.get('error')}")
        return
    
    record = record_data["medical_record"]
    
    st.success("✅ 电子病历生成完成！")
    st.markdown("---")
    
    # 使用选项卡展示不同部分
    tab1, tab2, tab3, tab4 = st.tabs(["📋 完整病历", " 分析结果", " 结构化数据", "💾 导出"])
    
    with tab1:
        st.subheader("📋 风湿免疫科电子病历")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**主诉:**")
            st.write(record.get("chief_complaint", "未生成"))
            
            st.markdown("**现病史:**")
            st.write(record.get("present_illness", "未生成"))
            
            st.markdown("**既往史:**")
            st.write(record.get("past_history", "未生成"))
        
        with col2:
            st.markdown("**体格检查:**")
            st.write(record.get("physical_examination", "未生成"))
            
            st.markdown("**辅助检查:**")
            st.write(record.get("auxiliary_examination", "未生成"))
            
            st.markdown("**诊断:**")
            st.write(record.get("diagnosis", "未生成"))
            
            st.markdown("**治疗方案:**")
            st.write(record.get("treatment_plan", "未生成"))
    
    with tab2:
        st.subheader("🔍 问诊分析结果")
        st.write(record_data.get("analysis", "无分析结果"))
    
    with tab3:
        st.subheader(" 结构化数据")
        st.json(record)
    
    with tab4:
        st.subheader(" 导出选项")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 导出为Word文档"):
                st.info("Word导出功能待实现")
        
        with col2:
            if st.button("📋 复制到剪贴板"):
                st.info("复制功能待实现")


import openai
import asyncio
from typing import Dict, Any

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
                "analysis": analysis_response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _call_llm(self, prompt: str) -> str:
        """调用大模型API"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.prompts.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # 降低随机性，提高一致性
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
        
        # 简单的文本解析逻辑
        lines = record_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 识别章节标题
            if any(keyword in line for keyword in ["主诉", "现病史", "既往史", "体格检查", "辅助检查", "诊断", "治疗"]):
                for key in sections.keys():
                    if any(keyword in line for keyword in ["主诉", "现病史", "既往史", "体格检查", "辅助检查", "诊断", "治疗"]):
                        current_section = key
                        break
            elif current_section:
                sections[current_section] += line + "\n"
        
        return sections


if __name__ == "__main__":
    main()
