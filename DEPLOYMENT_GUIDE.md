# Streamlit 部署指南

## 概述

本指南将帮助您在 Streamlit Cloud 上成功部署风湿免疫科电子病历生成系统，包括语音输入功能。

## 部署前准备

### 1. 代码优化
- ✅ 已移除 `pyaudio` 依赖（避免编译错误）
- ✅ 使用浏览器端录音（无需服务器端音频处理）
- ✅ 优化语音识别服务（仅使用必要的依赖）

### 2. 依赖包
确保 `requirements.txt` 包含以下依赖：
```
streamlit>=1.28.0
openai>=1.0.0
asyncio
pandas>=1.5.0
python-docx>=0.8.11
pyperclip>=1.8.2
SpeechRecognition>=3.10.0
requests>=2.28.0
```

## Streamlit Cloud 部署步骤

### 1. 准备代码仓库
确保您的代码已推送到 GitHub 仓库，包含以下文件：
- `rheumatology_ehr_app.py` - 主应用程序
- `voice_input_component.py` - 语音输入组件
- `streamlit_speech_service.py` - 语音识别服务
- `requirements.txt` - 依赖包列表
- `VOICE_INPUT_README.md` - 功能说明文档

### 2. 在 Streamlit Cloud 上部署

1. **访问 Streamlit Cloud**
   - 打开 [share.streamlit.io](https://share.streamlit.io)
   - 使用 GitHub 账号登录

2. **连接仓库**
   - 点击 "New app"
   - 选择您的 GitHub 仓库
   - 选择 `voice-input-feature` 分支

3. **配置应用**
   - **Main file path**: `rheumatology_ehr_app.py`
   - **Python version**: 3.9 或更高版本

4. **设置环境变量**（可选）
   - `OPENAI_API_KEY`: 您的 OpenAI API 密钥
   - `OPENAI_BASE_URL`: API 基础 URL

5. **部署应用**
   - 点击 "Deploy!"
   - 等待部署完成

### 3. 验证部署

部署完成后，您应该能够：
- ✅ 访问应用主页
- ✅ 使用语音输入功能
- ✅ 上传音频文件进行转换
- ✅ 生成电子病历

## 故障排除

### 常见问题

1. **依赖安装失败**
   ```
   解决方案：确保 requirements.txt 不包含 pyaudio
   ```

2. **语音识别不工作**
   ```
   解决方案：检查网络连接，Google Speech Recognition 需要网络访问
   ```

3. **录音功能不工作**
   ```
   解决方案：确保浏览器支持 MediaRecorder API，允许麦克风访问
   ```

4. **API 密钥错误**
   ```
   解决方案：在 Streamlit Cloud 中正确设置环境变量
   ```

### 调试步骤

1. **检查日志**
   - 在 Streamlit Cloud 中查看应用日志
   - 查找错误信息和警告

2. **测试功能**
   - 测试文本输入功能
   - 测试语音上传功能
   - 测试病历生成功能

3. **验证依赖**
   - 确保所有依赖包正确安装
   - 检查 Python 版本兼容性

## 性能优化

### 1. 缓存优化
```python
@st.cache_data
def load_speech_service():
    return create_streamlit_speech_service()
```

### 2. 错误处理
```python
try:
    # 语音识别代码
    pass
except Exception as e:
    st.error(f"语音识别失败: {str(e)}")
    # 提供备用方案
```

### 3. 用户体验
- 添加加载指示器
- 提供清晰的错误信息
- 支持重试机制

## 安全考虑

1. **API 密钥安全**
   - 使用环境变量存储敏感信息
   - 不要在代码中硬编码密钥

2. **用户隐私**
   - 录音文件仅在本地处理
   - 不存储用户音频数据

3. **网络安全**
   - 使用 HTTPS 连接
   - 验证用户输入

## 监控和维护

### 1. 应用监控
- 监控应用性能
- 检查错误日志
- 跟踪用户使用情况

### 2. 定期更新
- 更新依赖包
- 修复安全漏洞
- 优化性能

### 3. 用户反馈
- 收集用户反馈
- 改进用户体验
- 添加新功能

## 扩展功能

### 1. 多语言支持
- 支持更多语言识别
- 国际化界面

### 2. 高级语音识别
- 集成 Azure Speech Services
- 支持自定义词汇

### 3. 离线功能
- 本地语音识别
- 离线病历生成

## 联系支持

如果遇到部署问题，请：
1. 检查本文档的故障排除部分
2. 查看 Streamlit Cloud 文档
3. 提交 GitHub Issue

## 更新日志

- **v1.0.0**: 初始版本，支持基本语音输入
- **v1.1.0**: 优化 Streamlit 部署，移除 pyaudio 依赖
- **v1.2.0**: 添加多语言支持和错误处理 