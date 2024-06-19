import streamlit as st
import sys, os
sys.path.append(os.environ.get('PROJECT_BASE_DIR'))
from llm.adapter import to_prompt, SYSTEMS, DEFAULT_REQUIREMENTS

# set sessions
if st.session_state.get('pos_prompt') is None:
    st.session_state.pos_prompt = ''
    st.session_state.neg_prompt = ''
if st.session_state.get('system_prompt') is None:
    st.session_state.system_prompt = None
    st.session_state.theme = None

    
st.set_page_config(
    page_title="文本需求处理",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# page elements
st.title('用户需求 转换 绘图模型提示词')
# add a expander for modifing the system prompt

# first choose a theme
st.caption('请选择绘图主题')
st.session_state.theme = st.selectbox('绘图主题', list(SYSTEMS.keys()), index=0)
st.session_state.system_prompt = SYSTEMS[st.session_state.theme]

if st.session_state.system_prompt is not None:
    with st.expander('系统提示词'):
        # text area for inputing
        st.session_state.system_prompt = st.text_area('系统提示词', st.session_state.system_prompt, height=400, label_visibility="collapsed")
        # echo the system prompt as markdown
        st.caption('系统提示词 Markdown格式')
        st.markdown(st.session_state.system_prompt)


    input_col, button_col = st.columns([4, 1])
    with input_col:
        text_input = st.text_input('需求', DEFAULT_REQUIREMENTS[st.session_state.theme], label_visibility="collapsed")
    with button_col:
        if text_input:
            start_button = st.button('开始转换')
    if start_button:
        with st.spinner('正在生成提示词...'):
            pos_prompt, neg_prompt = to_prompt(text_input, prompt=st.session_state.system_prompt)
            if not pos_prompt:
                st.error('GLM输出格式有误，请重试')
            else:
                st.text('正向提示词')
                with st.container(border=True):
                    st.markdown(pos_prompt)
                st.text('反向提示词')
                with st.container(border=True):
                    st.markdown(neg_prompt)
                # pass to the next page
                st.session_state.pos_prompt = pos_prompt
                st.session_state.neg_prompt = neg_prompt
                # show info
                st.toast('提示词生成成功，已复制至绘图页面', icon='😀')
                st.page_link('pages/2_draw.py', label='前往画图页面', icon='🖌️', use_container_width=True)
