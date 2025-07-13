import streamlit as st
import asyncio
import openai
from typing import Dict, Any

# 页面配置
st.set_page_config(
    page_title="风湿免疫科电子病历生成系统 - 演示版",
    page_icon="🏥",
    layout="wide"
)

# 预设配置（演示用）
DEMO_API_KEY = "sk-CWTh6ygUZyDPjlVJB4C804F64dF140C89e984c848a4e3f7b"
DEMO_BASE_URL = "https://vip.apiyi.com/v1"

# 演示数据
DEMO_RECORDS = {
    "类风湿关节炎": "患者女性，45岁，主诉双手小关节疼痛、肿胀3个月，晨僵明显，持续时间约2小时，伴有乏力、食欲不振。既往无特殊病史。",
    "系统性红斑狼疮": "患者女性，28岁，主诉面部皮疹2个月，伴有光敏感、关节疼痛、脱发，近期出现发热、乏力。",
    "干燥综合征": "患者女性，52岁，主诉口干、眼干1年，伴有吞咽困难、关节疼痛，既往有甲状腺功能减退病史。"
}

# 模拟结果（演示用）
DEMO_RESULTS = {
    "类风湿关节炎": {
        "chief_complaint": "双手小关节疼痛、肿胀3个月，晨僵明显",
        "present_illness": "患者3个月前开始出现双手小关节疼痛、肿胀，晨僵明显，持续时间约2小时，伴有乏力、食欲不振。症状逐渐加重，影响日常生活。",
        "past_history": "既往无特殊病史",
        "physical_examination": "双手小关节肿胀、压痛，活动受限，晨僵明显",
        "auxiliary_examination": "建议检查：RF、抗CCP抗体、ESR、CRP、手部X线片",
        "diagnosis": "类风湿关节炎（待确诊）",
        "treatment_plan": "1. 非甾体抗炎药缓解症状\n2. 免疫抑制剂治疗\n3. 定期复查"
    },
    "系统性红斑狼疮": {
        "chief_complaint": "面部皮疹2个月，伴有光敏感、关节疼痛、脱发",
        "present_illness": "患者2个月前开始出现面部皮疹，伴有光敏感、关节疼痛、脱发，近期出现发热、乏力。症状逐渐加重。",
        "past_history": "既往无特殊病史",
        "physical_examination": "面部蝶形红斑，关节压痛，脱发明显",
        "auxiliary_examination": "建议检查：ANA、抗dsDNA抗体、补体C3/C4、血常规、尿常规",
        "diagnosis": "系统性红斑狼疮（待确诊）",
        "treatment_plan": "1. 糖皮质激素治疗\n2. 免疫抑制剂\n3. 避免阳光照射"
    },
    "干燥综合征": {
        "chief_complaint": "口干、眼干1年，伴有吞咽困难、关节疼痛",
        "present_illness": "患者1年前开始出现口干、眼干，伴有吞咽困难、关节疼痛，症状逐渐加重。",
        "past_history": "既往有甲状腺功能减退病史",
        "physical_examination": "口腔黏膜干燥，眼结膜充血，关节压痛",
        "auxiliary_examination": "建议检查：抗SSA/SSB抗体、泪液分泌试验、唾液腺功能检查",
        "diagnosis": "干燥综合征（待确诊）",
        "treatment_plan": "1. 人工泪液和唾液替代\n2. 免疫抑制剂治疗\n3. 定期眼科检查"
    }
}

def main():
    st.title("🏥 风湿免疫科电子病历生成系统 - 演示版")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("📋 演示选项")
        
        # 选择演示案例
        selected_case = st.selectbox(
            "选择演示案例:",
            list(DEMO_RECORDS.keys())
        )
        
        if st.button("加载演示案例"):
            st.session_state.demo_text = DEMO_RECORDS[selected_case]
            st.session_state.selected_case = selected_case
    
    # 主界面
    st.markdown("### 📝 问诊记录输入")
    
    # 获取演示文本
    default_text = getattr(st.session_state, 'demo_text', '')
    consultation_text = st.text_area(
        "请输入医生与患者的完整问诊记录:",
        value=default_text,
        height=200,
        placeholder="例如：患者主诉关节疼痛3个月，晨僵明显，伴有皮疹..."
    )
    
    # 生成按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 生成电子病历", type="primary", use_container_width=True):
            if consultation_text.strip():
                with st.spinner("正在生成风湿免疫科电子病历..."):
                    # 模拟API调用延迟
                    import time
                    time.sleep(2)
                    
                    # 获取演示结果
                    selected_case = getattr(st.session_state, 'selected_case', '类风湿关节炎')
                    demo_result = DEMO_RESULTS.get(selected_case, DEMO_RESULTS["类风湿关节炎"])
                    
                    display_demo_record(demo_result)
            else:
                st.error("请输入问诊记录")

def display_demo_record(record):
    st.success("✅ 电子病历生成完成！")
    st.markdown("---")
    
    st.markdown("### 📋 风湿免疫科电子病历")
    
    # 使用容器显示病历
    with st.container():
        st.markdown('<div style="background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 1.5rem; margin: 1rem 0;">', unsafe_allow_html=True)
        
        # 主诉
        st.markdown(f'''
        <div style="margin-bottom: 1.5rem; padding: 1rem; background-color: white; border-radius: 5px; border-left: 4px solid #007bff;">
            <div style="font-weight: bold; color: #007bff; margin-bottom: 0.5rem;">主诉</div>
            <div style="color: #333; line-height: 1.6;">{record["chief_complaint"]}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 现病史
        st.markdown(f'''
        <div style="margin-bottom: 1.5rem; padding: 1rem; background-color: white; border-radius: 5px; border-left: 4px solid #007bff;">
            <div style="font-weight: bold; color: #007bff; margin-bottom: 0.5rem;">现病史</div>
            <div style="color: #333; line-height: 1.6;">{record["present_illness"]}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 既往史
        st.markdown(f'''
        <div style="margin-bottom: 1.5rem; padding: 1rem; background-color: white; border-radius: 5px; border-left: 4px solid #007bff;">
            <div style="font-weight: bold; color: #007bff; margin-bottom: 0.5rem;">既往史</div>
            <div style="color: #333; line-height: 1.6;">{record["past_history"]}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 体格检查
        st.markdown(f'''
        <div style="margin-bottom: 1.5rem; padding: 1rem; background-color: white; border-radius: 5px; border-left: 4px solid #007bff;">
            <div style="font-weight: bold; color: #007bff; margin-bottom: 0.5rem;">体格检查</div>
            <div style="color: #333; line-height: 1.6;">{record["physical_examination"]}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 辅助检查
        st.markdown(f'''
        <div style="margin-bottom: 1.5rem; padding: 1rem; background-color: white; border-radius: 5px; border-left: 4px solid #007bff;">
            <div style="font-weight: bold; color: #007bff; margin-bottom: 0.5rem;">辅助检查</div>
            <div style="color: #333; line-height: 1.6;">{record["auxiliary_examination"]}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 诊断
        st.markdown(f'''
        <div style="margin-bottom: 1.5rem; padding: 1rem; background-color: white; border-radius: 5px; border-left: 4px solid #007bff;">
            <div style="font-weight: bold; color: #007bff; margin-bottom: 0.5rem;">诊断</div>
            <div style="color: #333; line-height: 1.6;">{record["diagnosis"]}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 治疗方案
        st.markdown(f'''
        <div style="margin-bottom: 1.5rem; padding: 1rem; background-color: white; border-radius: 5px; border-left: 4px solid #007bff;">
            <div style="font-weight: bold; color: #007bff; margin-bottom: 0.5rem;">治疗方案</div>
            <div style="color: #333; line-height: 1.6;">{record["treatment_plan"]}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 底部说明
    st.markdown("---")
    st.info("💡 这是演示版本，实际应用需要配置有效的API密钥才能调用真实的AI模型。")

if __name__ == "__main__":
    main() 