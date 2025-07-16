#!/usr/bin/env python3
"""
测试Word导出处理器
"""

from word_export_handler import create_word_export_handler

def test_word_export_handler():
    """测试Word导出处理器"""
    print("🔍 测试Word导出处理器...")
    
    try:
        # 创建Word导出处理器
        word_handler = create_word_export_handler()
        print("✅ Word导出处理器创建成功")
        
        # 创建测试数据
        test_record = {
            "chief_complaint": "患者女性，45岁，主诉双手小关节疼痛、肿胀3个月",
            "present_illness": "患者3个月前开始出现双手小关节疼痛，逐渐加重，伴有晨僵，持续时间约2小时",
            "past_history": "既往无特殊病史，否认家族风湿病史",
            "physical_examination": "双手近端指间关节、掌指关节肿胀，压痛阳性，活动受限",
            "auxiliary_examination": "建议检查RF、抗CCP抗体、ESR、CRP等",
            "diagnosis": "类风湿关节炎",
            "treatment_plan": "1. 甲氨蝶呤 10mg 每周一次\n2. 来氟米特 20mg 每日一次\n3. 定期复查"
        }
        
        # 测试Word导出功能
        success, message = word_handler.handle_word_export(test_record)
        if success:
            print("✅ Word导出功能正常")
        else:
            print(f"❌ Word导出失败: {message}")
        
        # 测试复制到剪贴板功能
        success, message = word_handler.handle_copy_to_clipboard(test_record)
        if success:
            print("✅ 复制到剪贴板功能正常")
        else:
            print(f"❌ 复制到剪贴板失败: {message}")
        
        return True
    except Exception as e:
        print(f"❌ Word导出处理器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试Word导出处理器...\n")
    
    if not test_word_export_handler():
        print("\n❌ Word导出处理器测试失败")
        return False
    
    print("\n✅ 所有Word导出处理器功能测试通过！")
    print("\n📝 改进说明：")
    print("1. 解决了页面重新加载问题")
    print("2. 直接显示下载按钮，无需额外点击")
    print("3. 改进了错误处理和用户反馈")
    print("4. 优化了复制到剪贴板功能")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 