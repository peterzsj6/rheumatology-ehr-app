# 风湿免疫科电子病历生成系统

一个基于大模型API的风湿免疫科专业电子病历生成系统，能够根据医生与患者的问诊记录自动生成标准化的电子病历。

## 功能特点

- 🏥 **专业性强**: 专门针对风湿免疫科设计
- 🤖 **AI驱动**: 基于GPT-4大模型
- 📝 **标准化**: 生成符合医疗规范的电子病历
- 🎨 **用户友好**: 现代化的Web界面
- 📊 **多视图**: 支持完整病历、分析结果、结构化数据等多种展示方式

## 系统要求

- Python 3.8+
- OpenAI API Key
- 网络连接

## 安装步骤

### 1. 克隆或下载项目
```bash
git clone <repository-url>
cd rheumatology-ehr-system
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

#### 本地开发
```bash
# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_BASE_URL="https://vip.apiyi.com/v1"

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
$env:OPENAI_BASE_URL="https://vip.apiyi.com/v1"

# Windows (CMD)
set OPENAI_API_KEY=your-api-key-here
set OPENAI_BASE_URL=https://vip.apiyi.com/v1
```

#### Streamlit Cloud部署
1. 将代码推送到GitHub
2. 在[Streamlit Cloud](https://streamlit.io/cloud)创建新应用
3. 在应用设置中配置Secrets：
```
OPENAI_API_KEY = "your-api-key-here"
OPENAI_BASE_URL = "https://vip.apiyi.com/v1"
```

#### 手动输入
在运行应用时，在侧边栏输入你的OpenAI API密钥。

## 运行应用

### 本地运行
```bash
# 直接运行
streamlit run rheumatology_ehr_app.py

# 指定端口运行
streamlit run rheumatology_ehr_app.py --server.port 8501

# 后台运行
nohup streamlit run rheumatology_ehr_app.py > app.log 2>&1 &
```

### 云端部署

#### Streamlit Cloud部署
1. **推送代码到GitHub**
   ```bash
   git add .
   git commit -m "Add Streamlit app"
   git push origin main
   ```

2. **在Streamlit Cloud创建应用**
   - 访问 [Streamlit Cloud](https://streamlit.io/cloud)
   - 点击 "New app"
   - 选择你的GitHub仓库
   - 设置主文件路径为 `rheumatology_ehr_app.py`

3. **配置Secrets**
   - 在应用设置页面点击 "Secrets"
   - 添加以下配置：
   ```
   OPENAI_API_KEY = "your-api-key-here"
   OPENAI_BASE_URL = "https://vip.apiyi.com/v1"
   ```

4. **部署应用**
   - 点击 "Deploy" 按钮
   - 等待部署完成
   - 访问生成的URL

#### 其他平台部署
- **Heroku**: 使用 `requirements.txt` 和 `Procfile`
- **Docker**: 使用提供的 `Dockerfile`
- **VPS**: 直接运行 `streamlit run` 命令

## 使用说明

### 1. 启动应用
运行上述命令后，应用将在浏览器中自动打开，通常地址为 `http://localhost:8501`

### 2. 配置API
- 在侧边栏输入你的OpenAI API密钥
- 选择合适的基础URL（如果使用自定义API端点）
- 调整模型参数（温度、模型选择等）

### 3. 输入问诊记录
- 在文本框中输入医生与患者的问诊记录
- 可以使用侧边栏的示例记录进行测试
- 支持中文输入

### 4. 生成电子病历
- 点击"生成电子病历"按钮
- 系统将分析问诊内容并生成结构化病历
- 结果将在多个选项卡中展示

### 5. 查看结果
- **完整病历**: 查看生成的完整电子病历
- **分析结果**: 查看AI对问诊记录的分析
- **结构化数据**: 查看JSON格式的结构化数据
- **导出选项**: 导出和复制功能

## 示例问诊记录

系统内置了三个示例问诊记录：

1. **类风湿关节炎**: 关节疼痛、晨僵等症状
2. **系统性红斑狼疮**: 皮疹、光敏感等症状
3. **干燥综合征**: 口干、眼干等症状

## 生成的病历结构

系统生成的电子病历包含以下部分：

- **主诉**: 患者主要症状
- **现病史**: 症状发展过程
- **既往史**: 相关病史
- **体格检查**: 检查发现
- **辅助检查**: 建议的实验室和影像学检查
- **诊断**: 初步诊断和鉴别诊断
- **治疗方案**: 治疗建议

## 技术架构

- **前端**: Streamlit
- **后端**: Python + OpenAI API
- **AI模型**: GPT-4
- **数据处理**: 异步处理
- **界面设计**: 响应式布局

## 注意事项

1. **API密钥安全**: 请妥善保管你的API密钥，不要泄露给他人
2. **网络连接**: 确保网络连接稳定，以便正常调用API
3. **数据隐私**: 本系统仅处理文本数据，不会存储敏感医疗信息
4. **专业建议**: 生成的病历仅供参考，实际医疗决策需要专业医生判断

## 故障排除

### 常见问题

1. **API调用失败**
   - 检查API密钥是否正确
   - 确认网络连接正常
   - 验证API端点URL是否正确

2. **应用无法启动**
   - 确认Python版本符合要求
   - 检查依赖包是否正确安装
   - 查看错误日志

3. **生成结果不理想**
   - 尝试调整温度参数
   - 使用更详细的问诊记录
   - 检查输入文本的完整性

## 开发计划

- [ ] 添加更多专科支持
- [ ] 实现Word文档导出功能
- [ ] 添加病历模板管理
- [ ] 集成数据库存储
- [ ] 添加用户认证系统
- [ ] 实现批量处理功能

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

本项目采用MIT许可证。 