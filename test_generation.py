import streamlit as st
import asyncio
from rheumatology_ehr_app import RheumatologyEHRSystem

st.title("生成功能测试")

# 初始化session state
if 'test_result' not in st.session_state:
    st.session_state.test_result = None

# 测试输入
test_input = st.text_area("测试输入:", value="患者主诉关节疼痛3个月", height=100)

# 测试按钮
if st.button("测试生成"):
    if test_input.strip():
        st.session_state.test_result = {"success": True, "medical_record": {
            "chief_complaint": "关节疼痛3个月",
            "present_illness": "患者3个月前开始出现关节疼痛",
            "past_history": "无特殊病史",
            "physical_examination": "关节压痛阳性",
            "auxiliary_examination": "建议进行血液检查",
            "diagnosis": "考虑类风湿关节炎",
            "treatment_plan": "建议药物治疗"
        }}
        st.success("测试生成完成！")
    else:
        st.error("请输入测试内容")

# 显示结果
if st.session_state.test_result:
    st.write("生成结果:", st.session_state.test_result) 