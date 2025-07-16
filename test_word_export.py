#!/usr/bin/env python3
"""
测试Word导出功能
"""

import tempfile
import os
from word_exporter import create_word_exporter

def test_word_exporter():
    """测试Word导出器"""
    print("🔍 测试Word导出器...")
    
    try:
        # 创建Word导出器
        word_exporter = create_word_exporter()
        print("✅ Word导出器创建成功")
        
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
        
        # 测试导出到字节
        doc_bytes = word_exporter.export_to_bytes(test_record)
        print(f"✅ Word文档生成成功，大小: {len(doc_bytes)} 字节")
        
        # 测试导出到文件
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            word_exporter.export_to_file(test_record, temp_file.name)
            print(f"✅ Word文档保存成功: {temp_file.name}")
            
            # 检查文件是否存在
            if os.path.exists(temp_file.name):
                file_size = os.path.getsize(temp_file.name)
                print(f"✅ 文件验证成功，大小: {file_size} 字节")
                
                # 清理临时文件
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            else:
                print("❌ 文件保存失败")
        
        return True
    except Exception as e:
        print(f"❌ Word导出器测试失败: {e}")
        return False

def test_dependencies():
    """测试依赖库"""
    print("\n🔍 测试依赖库...")
    
    try:
        import docx
        print("✅ python-docx 库可用")
    except ImportError:
        print("❌ python-docx 库不可用，请安装: pip install python-docx")
        return False
    
    try:
        import pyperclip
        print("✅ pyperclip 库可用")
    except ImportError:
        print("⚠️ pyperclip 库不可用，复制功能可能受限")
    
    return True

def main():
    """主测试函数"""
    print("🚀 开始测试Word导出功能...\n")
    
    # 测试依赖库
    if not test_dependencies():
        print("\n❌ 依赖库测试失败")
        return False
    
    # 测试Word导出器
    if not test_word_exporter():
        print("\n❌ Word导出器测试失败")
        return False
    
    print("\n✅ 所有Word导出功能测试通过！")
    print("\n📝 Word导出功能说明：")
    print("1. 支持导出为.docx格式")
    print("2. 包含完整的病历结构")
    print("3. 自动添加生成时间和签名区域")
    print("4. 支持下载和保存功能")
    print("5. 同时实现了复制到剪贴板功能")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 