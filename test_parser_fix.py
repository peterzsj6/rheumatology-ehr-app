import streamlit as st

st.title("解析逻辑修复测试")

# 测试文本（基于您提供的实际输出）
test_text = st.text_area(
    "测试文本:",
    value="""主诉：

手腕和手指关节晨僵三个月，双膝关节肿痛一周，伴有低烧和皮疹。

现病史：

患者三个月前开始出现手腕和手指关节晨僵，持续半小时以上。一周前双膝关节出现肿痛，活动受限，伴有低烧。皮疹在晒太阳后加重。

既往史：

母亲有类风湿关节炎病史。

体格检查：

关节检查：手腕、手指、双膝关节肿胀、压痛，活动受限。
皮肤黏膜：红色皮疹，晒太阳后加重。
心肺：未及明显异常。

辅助检查：

实验室检查：类风湿因子偏高，血沉40mm/h。
影像学检查：待查。

诊断：

类风湿关节炎：对称性多关节炎，晨僵>1小时，RF阳性，家族史。
系统性红斑狼疮：皮疹，光敏感，低烧，需进一步检查ANA等自身抗体。

治疗方案：

药物治疗：非甾体抗炎药（NSAIDs）缓解症状，考虑使用疾病修饰抗风湿药（DMARDs）如甲氨蝶呤。
非药物治疗：物理治疗，关节保护。
监测方案：定期监测血常规、肝功能、肾功能、疾病活动度。
随访计划：每月随访，评估治疗效果和调整治疗方案。""",
    height=400
)

def parse_record_text(record_text: str):
    """修复后的解析逻辑"""
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
    
    # 定义章节标题映射
    section_mapping = {
        "主诉": "chief_complaint",
        "主诉：": "chief_complaint",
        "现病史": "present_illness", 
        "现病史：": "present_illness",
        "既往史": "past_history",
        "既往史：": "past_history",
        "体格检查": "physical_examination",
        "体格检查：": "physical_examination",
        "辅助检查": "auxiliary_examination",
        "辅助检查：": "auxiliary_examination",
        "诊断": "diagnosis",
        "诊断：": "diagnosis",
        "治疗方案": "treatment_plan",
        "治疗方案：": "treatment_plan"
    }
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 跳过空行
        if not line:
            i += 1
            continue
        
        # 检查是否是新的章节标题
        found_section = None
        for prefix, section_key in section_mapping.items():
            if line.startswith(prefix):
                found_section = section_key
                break
        
        if found_section:
            # 保存之前章节的内容
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
                st.write(f"保存章节 '{current_section}': {sections[current_section][:50]}...")
                current_content = []
            
            # 设置新的章节
            current_section = found_section
            st.write(f"新章节: '{current_section}'")
            
            # 跳过章节标题行和可能的空行
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            continue
        
        # 如果不是章节标题，且当前有活跃章节，则添加内容
        elif current_section and line:
            # 过滤掉一些不需要的内容
            skip_prefixes = ["[", "请", "注意", "基于", "请严格按照", "注意：", "电子病历生成"]
            if not any(line.startswith(prefix) for prefix in skip_prefixes):
                current_content.append(line)
        
        i += 1
    
    # 保存最后一个章节的内容
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
        st.write(f"保存最后章节 '{current_section}': {sections[current_section][:50]}...")
    
    # 确保所有章节都有内容，如果没有则设置为"无"
    for key in sections:
        if not sections[key].strip():
            sections[key] = "无"
    
    return sections

if st.button("测试解析"):
    result = parse_record_text(test_text)
    st.write("### 解析结果:")
    for key, value in result.items():
        st.write(f"**{key}**: {value}") 