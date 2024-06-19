import streamlit as st

# TODO: add welcome page

st.set_page_config(
    page_title="灵制-模型Demo",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# show balloons
st.balloons()

st.markdown(
"""
# 灵制-模型Demo
欢迎来到灵制项目的模型部分，这里提供了一些模型的在线演示，包括：
- 用户自然语言需求 转换为 Stable Diffusion提示词
- Stable Diffusion提示词 生成图片
- 图片转3D模型
- 3D模型贴图
"""
)

st.markdown(
"""
#### 选择功能
"""
)

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.page_link('pages/1_prompt.py', label='需求转提示词', icon='🖊️')
with col2:
    st.page_link('pages/2_draw.py', label='绘图', icon='🖼️')
with col3:
    st.page_link('pages/4_pic2model.py', label='图片转3D', icon='🎨')
with col4:
    st.page_link('pages/3_render.py', label='3D贴图', icon='🖌️')
