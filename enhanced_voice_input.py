import streamlit as st
import streamlit.components.v1 as components
from streamlit_speech_service import create_streamlit_speech_service
import tempfile
import os
import base64
import json

def enhanced_voice_input_component():
    """增强的语音输入组件，支持自动转换"""
    
    # HTML和JavaScript代码
    html_code = """
    <div id="enhanced-voice-input-container">
        <button id="start-recording" onclick="startRecording()" style="
            background-color: #007bff; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer;
            margin: 5px;
        ">🎤 开始录音</button>
        
        <button id="stop-recording" onclick="stopRecording()" style="
            background-color: #dc3545; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer;
            margin: 5px;
            display: none;
        ">⏹️ 停止录音</button>
        
        <div id="recording-status" style="
            text-align: center; 
            color: red; 
            font-size: 1.2rem; 
            margin: 10px 0;
            display: none;
        ">⏺️ 录音中...</div>
        
        <div id="transcription-result" style="
            margin: 10px 0; 
            padding: 10px; 
            background-color: #f8f9fa; 
            border-radius: 5px;
            display: none;
        "></div>
        
        <div id="auto-convert-status" style="
            text-align: center; 
            color: #28a745; 
            font-size: 1rem; 
            margin: 10px 0;
            display: none;
        ">🔄 正在自动转换语音...</div>
    </div>

    <script>
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let recordingStartTime;

    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    sampleRate: 16000,
                    channelCount: 1,
                    echoCancellation: true,
                    noiseSuppression: true
                } 
            });
            
            // 使用正确的MIME类型
            const mimeType = 'audio/webm;codecs=opus';
            mediaRecorder = new MediaRecorder(stream, { mimeType: mimeType });
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: mimeType });
                
                // 显示录音结果
                document.getElementById('transcription-result').innerHTML = 
                    '<strong>录音完成！</strong><br>' +
                    '<audio controls><source src="' + URL.createObjectURL(audioBlob) + '" type="' + mimeType + '"></audio><br>';
                document.getElementById('transcription-result').style.display = 'block';
                
                // 显示自动转换状态
                document.getElementById('auto-convert-status').style.display = 'block';
                document.getElementById('auto-convert-status').textContent = '🔄 正在自动转换语音...';
                
                // 自动转换音频
                await autoConvertAudio(audioBlob);
            };
            
            mediaRecorder.start();
            isRecording = true;
            recordingStartTime = Date.now();
            
            // 更新UI
            document.getElementById('start-recording').style.display = 'none';
            document.getElementById('stop-recording').style.display = 'inline-block';
            document.getElementById('recording-status').style.display = 'block';
            
            // 更新录音时间
            updateRecordingTime();
            
        } catch (error) {
            alert('无法访问麦克风: ' + error.message);
        }
    }
    
    function stopRecording() {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
            isRecording = false;
            
            // 更新UI
            document.getElementById('start-recording').style.display = 'inline-block';
            document.getElementById('stop-recording').style.display = 'none';
            document.getElementById('recording-status').style.display = 'none';
        }
    }
    
    function updateRecordingTime() {
        if (isRecording) {
            const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
            document.getElementById('recording-status').textContent = `⏺️ 录音中... ${elapsed}秒`;
            setTimeout(updateRecordingTime, 1000);
        }
    }
    
    async function autoConvertAudio(audioBlob) {
        try {
            // 将音频转换为base64
            const arrayBuffer = await audioBlob.arrayBuffer();
            const base64Audio = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
            
            // 发送到Streamlit进行转换
            const data = {
                audio_data: base64Audio,
                audio_type: audioBlob.type,
                language: 'zh-CN'
            };
            
            // 使用Streamlit的组件通信
            window.parent.postMessage({
                type: 'AUDIO_CONVERSION_REQUEST',
                data: data
            }, '*');
            
        } catch (error) {
            console.error('音频转换失败:', error);
            document.getElementById('auto-convert-status').textContent = '❌ 音频转换失败';
        }
    }
    
    // 监听来自Streamlit的消息
    window.addEventListener('message', function(event) {
        if (event.data.type === 'AUDIO_CONVERSION_RESULT') {
            const result = event.data.data;
            if (result.success) {
                document.getElementById('auto-convert-status').textContent = '✅ 语音转换完成！';
                // 可以在这里显示转换结果
            } else {
                document.getElementById('auto-convert-status').textContent = '❌ 语音转换失败: ' + result.error;
            }
        }
    });
    </script>
    """
    
    # 渲染组件
    components.html(html_code, height=400)

def enhanced_voice_input_section():
    """增强的语音输入区域"""
    st.markdown('<h3 class="section-header">🎤 语音输入（增强版）</h3>', unsafe_allow_html=True)
    
    # 语音输入说明
    st.info("""
    **增强版语音输入功能：**
    1. 点击"开始录音"按钮开始录音
    2. 说话完成后点击"停止录音"
    3. 系统会自动转换语音为文字
    4. 转换结果会自动填入问诊记录输入框
    """)
    
    # 渲染增强的语音输入组件
    enhanced_voice_input_component()
    
    st.markdown("---")
    st.markdown("**或者直接上传音频文件：**")
    
    # 文件上传器
    uploaded_audio = st.file_uploader(
        "上传音频文件（支持WAV、MP3、WebM格式）",
        type=['wav', 'mp3', 'webm', 'ogg'],
        key="enhanced_audio_uploader"
    )
    
    if uploaded_audio is not None:
        st.success(f"已上传音频文件: {uploaded_audio.name}")
        
        # 显示音频播放器
        st.audio(uploaded_audio, format='audio/wav')
        
        # 语音识别服务配置
        st.markdown("**语音识别服务配置：**")
        col1, col2 = st.columns(2)
        
        with col1:
            service_type = st.selectbox(
                "选择语音识别服务：",
                ["google", "azure", "baidu", "tencent"],
                format_func=lambda x: {
                    "google": "Google Speech Recognition",
                    "azure": "Azure Speech Services", 
                    "baidu": "百度语音识别",
                    "tencent": "腾讯语音识别"
                }[x],
                key="enhanced_service_type"
            )
        
        with col2:
            language = st.selectbox(
                "选择语言：",
                ["zh-CN", "zh-TW", "en-US", "en-GB"],
                format_func=lambda x: {
                    "zh-CN": "中文（简体）",
                    "zh-TW": "中文（繁体）", 
                    "en-US": "英语（美国）",
                    "en-GB": "英语（英国）"
                }[x],
                key="enhanced_language"
            )
        
        # 转换按钮
        if st.button("🎵 转换语音为文字", key="enhanced_convert_audio"):
            with st.spinner("正在转换语音..."):
                try:
                    # 创建语音识别服务
                    speech_service = create_streamlit_speech_service(service_type=service_type)
                    
                    # 处理不同格式的音频文件
                    audio_data = uploaded_audio.getvalue()
                    file_extension = uploaded_audio.name.split('.')[-1].lower()
                    
                    # 根据文件格式选择正确的后缀
                    if file_extension in ['mp3', 'webm', 'ogg']:
                        suffix = f".{file_extension}"
                    else:
                        suffix = ".wav"
                    
                    # 转换音频文件
                    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
                        temp_file.write(audio_data)
                        temp_audio_path = temp_file.name
                    
                    # 进行语音识别
                    transcribed_text = speech_service.transcribe_audio_file(temp_audio_path, language)
                    
                    # 清理临时文件
                    try:
                        os.unlink(temp_audio_path)
                    except:
                        pass
                    
                    # 保存结果
                    st.session_state.transcribed_text = transcribed_text
                    st.success("语音转换完成！")
                    
                    # 自动填入问诊记录输入框
                    if "example_text" not in st.session_state:
                        st.session_state.example_text = ""
                    st.session_state.example_text = transcribed_text
                    
                except Exception as e:
                    st.error(f"语音转换失败: {str(e)}")
                    # 如果转换失败，提供示例文字
                    st.session_state.transcribed_text = "患者主诉关节疼痛3个月，晨僵明显，伴有皮疹和发热症状。"
                    st.info("已提供示例文字，您可以编辑后使用。")
    
    # 显示转换后的文字
    if hasattr(st.session_state, 'transcribed_text'):
        st.markdown("### 转换结果：")
        st.text_area("语音转换文字：", value=st.session_state.transcribed_text, height=100, key="enhanced_transcribed_text_area")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 使用此文字", key="enhanced_use_transcribed_text"):
                st.session_state.example_text = st.session_state.transcribed_text
                st.success("已使用转换的文字！")
        with col2:
            if st.button("🔄 重新转换", key="enhanced_retry_transcription"):
                del st.session_state.transcribed_text
                st.rerun() 