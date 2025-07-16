import streamlit as st
import streamlit.components.v1 as components
from streamlit_speech_service import create_streamlit_speech_service
import tempfile
import os
import base64

def simple_voice_input_component():
    """简化的语音输入组件，使用更可靠的通信机制"""
    
    # HTML和JavaScript代码
    html_code = """
    <div id="simple-voice-input-container">
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
        
        <div id="recording-result" style="
            margin: 10px 0; 
            padding: 10px; 
            background-color: #f8f9fa; 
            border-radius: 5px;
            display: none;
        "></div>
        
        <div id="conversion-status" style="
            text-align: center; 
            color: #28a745; 
            font-size: 1rem; 
            margin: 10px 0;
            display: none;
        ">🔄 正在转换语音...</div>
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
            
            // 使用WebM格式，浏览器原生支持
            const mimeType = 'audio/webm;codecs=opus';
            mediaRecorder = new MediaRecorder(stream, { mimeType: mimeType });
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: mimeType });
                
                // 显示录音结果
                const audioUrl = URL.createObjectURL(audioBlob);
                document.getElementById('recording-result').innerHTML = 
                    '<strong>录音完成！</strong><br>' +
                    '<audio controls><source src="' + audioUrl + '" type="' + mimeType + '"></audio><br>' +
                    '<button onclick="downloadAudio()" style="background-color: #28a745; color: white; border: none; padding: 8px 16px; border-radius: 4px; margin: 5px;">📥 下载录音</button>' +
                    '<button onclick="convertAudio()" style="background-color: #007bff; color: white; border: none; padding: 8px 16px; border-radius: 4px; margin: 5px;">🎵 转换语音</button>';
                document.getElementById('recording-result').style.display = 'block';
                
                // 保存音频数据到全局变量
                window.recordedAudioBlob = audioBlob;
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
    
    function downloadAudio() {
        if (window.recordedAudioBlob) {
            const url = URL.createObjectURL(window.recordedAudioBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'recording.webm';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    }
    
    function convertAudio() {
        if (!window.recordedAudioBlob) {
            alert('没有可转换的录音');
            return;
        }
        
        // 显示转换状态
        document.getElementById('conversion-status').style.display = 'block';
        document.getElementById('conversion-status').textContent = '🔄 正在转换语音...';
        
        // 模拟转换过程（实际转换在Streamlit后端进行）
        setTimeout(() => {
            document.getElementById('conversion-status').textContent = '✅ 请上传录音文件进行转换';
        }, 2000);
    }
    </script>
    """
    
    # 渲染组件
    components.html(html_code, height=350)

def simple_voice_input_section():
    """简化的语音输入区域"""
    st.markdown('<h3 class="section-header">🎤 语音输入（简化版）</h3>', unsafe_allow_html=True)
    
    # 语音输入说明
    st.info("""
    **简化版语音输入功能：**
    1. 点击"开始录音"按钮开始录音
    2. 说话完成后点击"停止录音"
    3. 下载录音文件后上传进行转换
    4. 或直接使用文本输入功能
    """)
    
    # 渲染简化的语音输入组件
    simple_voice_input_component()
    
    st.markdown("---")
    st.markdown("**上传音频文件进行转换：**")
    
    # 文件上传器
    uploaded_audio = st.file_uploader(
        "上传音频文件（支持WAV、MP3、WebM格式）",
        type=['wav', 'mp3', 'webm', 'ogg'],
        key="simple_audio_uploader"
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
                key="simple_service_type"
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
                key="simple_language"
            )
        
        # 转换按钮
        if st.button("🎵 转换语音为文字", key="simple_convert_audio"):
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
        st.text_area("语音转换文字：", value=st.session_state.transcribed_text, height=100, key="simple_transcribed_text_area")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 使用此文字", key="simple_use_transcribed_text"):
                st.session_state.example_text = st.session_state.transcribed_text
                st.success("已使用转换的文字！")
        with col2:
            if st.button("🔄 重新转换", key="simple_retry_transcription"):
                del st.session_state.transcribed_text
                st.rerun() 