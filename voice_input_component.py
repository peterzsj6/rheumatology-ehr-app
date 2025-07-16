import streamlit as st
import streamlit.components.v1 as components
from speech_recognition_service import create_speech_recognition_service
import tempfile
import os

def voice_input_component():
    """语音输入组件"""
    
    # HTML和JavaScript代码
    html_code = """
    <div id="voice-input-container">
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
    </div>

    <script>
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let recordingStartTime;

    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                
                // 显示录音结果
                document.getElementById('transcription-result').innerHTML = 
                    '<strong>录音完成！</strong><br>' +
                    '<audio controls><source src="' + audioUrl + '" type="audio/wav"></audio><br>' +
                    '<p>由于浏览器限制，无法直接进行语音识别。<br>' +
                    '请下载音频文件后上传到系统进行转换。</p>';
                document.getElementById('transcription-result').style.display = 'block';
                
                // 创建下载链接
                const downloadLink = document.createElement('a');
                downloadLink.href = audioUrl;
                downloadLink.download = 'recording.wav';
                downloadLink.textContent = '📥 下载录音文件';
                downloadLink.style.cssText = 'display: inline-block; margin: 10px; padding: 8px 16px; background-color: #28a745; color: white; text-decoration: none; border-radius: 4px;';
                document.getElementById('transcription-result').appendChild(downloadLink);
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
    </script>
    """
    
    # 渲染组件
    components.html(html_code, height=300)

def voice_input_section():
    """语音输入区域"""
    st.markdown('<h3 class="section-header">🎤 语音输入</h3>', unsafe_allow_html=True)
    
    # 语音输入说明
    st.info("""
    **语音输入功能说明：**
    1. 点击"开始录音"按钮开始录音
    2. 说话完成后点击"停止录音"
    3. 下载录音文件后上传到系统进行文字转换
    4. 或者直接使用文本输入功能
    """)
    
    # 渲染语音输入组件
    voice_input_component()
    
    st.markdown("---")
    st.markdown("**或者直接上传音频文件：**")
    
    # 文件上传器
    uploaded_audio = st.file_uploader(
        "上传音频文件（支持WAV、MP3格式）",
        type=['wav', 'mp3'],
        key="audio_uploader"
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
                }[x]
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
                }[x]
            )
        
        # 转换按钮
        if st.button("🎵 转换语音为文字", key="convert_audio"):
            with st.spinner("正在转换语音..."):
                try:
                    # 创建语音识别服务
                    speech_service = create_speech_recognition_service(service_type=service_type)
                    
                    # 转换音频文件
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                        temp_file.write(uploaded_audio.getvalue())
                        temp_audio_path = temp_file.name
                    
                    # 进行语音识别
                    transcribed_text = speech_service.transcribe_audio_file(temp_audio_path, language)
                    
                    # 清理临时文件
                    os.unlink(temp_audio_path)
                    
                    # 保存结果
                    st.session_state.transcribed_text = transcribed_text
                    st.success("语音转换完成！")
                    
                except Exception as e:
                    st.error(f"语音转换失败: {str(e)}")
                    # 如果转换失败，提供示例文字
                    st.session_state.transcribed_text = "患者主诉关节疼痛3个月，晨僵明显，伴有皮疹和发热症状。"
                    st.info("已提供示例文字，您可以编辑后使用。") 