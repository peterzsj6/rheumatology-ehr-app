import streamlit as st

st.title("文本解析调试工具")

# 测试文本
test_text = st.text_area(
    "输入LLM返回的原始文本:",
    value="""主诉：
患者主诉关节疼痛3个月

现病史：
患者3个月前开始出现关节疼痛，晨僵明显

既往史：
无特殊病史

体格检查：
关节压痛阳性

辅助检查：
建议进行血液检查

诊断：
考虑类风湿关节炎

治疗方案：
建议药物治疗""",
    height=300
)

def parse_record_text(record_text: str):
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
    
    st.write("### 解析过程:")
    st.write("原始行数:", len(lines))
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        st.write(f"行 {i+1}: '{line}'")
        
        # 检查是否是新的章节标题（支持多种格式）
        if any(line.startswith(prefix) for prefix in ["主诉：", "主诉", "现病史：", "现病史", "既往史：", "既往史", "体格检查：", "体格检查", "辅助检查：", "辅助检查", "诊断：", "诊断", "治疗方案：", "治疗方案"]):
            # 保存之前章节的内容
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
                st.write(f"保存章节 '{current_section}': {sections[current_section]}")
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
            
            st.write(f"新章节: '{current_section}'")
        
        # 如果不是章节标题，且当前有活跃章节，则添加内容
        elif current_section and line and not line.startswith("[") and not line.startswith("请") and not line.startswith("注意") and not line.startswith("基于"):
            current_content.append(line)
            st.write(f"添加到章节 '{current_section}': '{line}'")
    
    # 保存最后一个章节的内容
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
        st.write(f"保存最后章节 '{current_section}': {sections[current_section]}")
    
    # 确保所有章节都有内容，如果没有则设置为"无"
    for key in sections:
        if not sections[key].strip():
            sections[key] = "无"
    
    return sections

if st.button("解析文本"):
    result = parse_record_text(test_text)
    st.write("### 解析结果:")
    st.json(result) 