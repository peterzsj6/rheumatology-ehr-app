import streamlit as st

st.title("Session State 调试测试")

# 初始化session state
if 'test_value' not in st.session_state:
    st.session_state.test_value = None

# 显示当前session state
st.write("当前session state:", st.session_state.test_value)

# 测试按钮
if st.button("设置测试值"):
    st.session_state.test_value = "测试成功！"
    st.rerun()

# 显示结果
if st.session_state.test_value:
    st.success(f"结果: {st.session_state.test_value}") 