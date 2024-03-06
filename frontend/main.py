import streamlit as st
import os
import time
# add the project base dir to the path
import sys
sys.path.append(os.environ.get('PROJECT_BASE_DIR'))
from llm.adapter import to_prompt
from text2img.adapter import sd_default, save_encoded_image

DEFAULT_DIR = "./pics"
if not os.path.exists(DEFAULT_DIR):
    os.makedirs(DEFAULT_DIR)

# sessions
# record the pos_prompt and neg_prompt, triggered by the copy button
if 'pos_prompt' not in st.session_state:
    st.session_state.pos_prompt = ""
if 'neg_prompt' not in st.session_state:
    st.session_state.neg_prompt = ""

# three tabs
st.title('Lingzhi Model Service')
prompt_tab, draw_tab, modeling_tab = st.tabs(['Prompt', 'Draw', 'Modeling'])

with prompt_tab:
    st.write('需求转提示词')
    input_col, button_col = st.columns([4, 1])
    with input_col:
        text_input = st.text_input('需求', '画一只猫', label_visibility="collapsed")
    with button_col:
        if text_input:
            start_button = st.button('开始转换')
    if start_button:
        with st.spinner('Generating...'):
            pos_prompt, neg_prompt = to_prompt(text_input)
            if not pos_prompt:
                st.error('GLM输出格式有误，请重试')
            else:
                st.subheader('正向提示词')
                st.markdown(pos_prompt)
                st.subheader('反向提示词')
                st.markdown(neg_prompt)
                st.session_state.pos_prompt = pos_prompt
                st.session_state.neg_prompt = neg_prompt
                # show info
                st.info('已复制到画图，点击Draw标签继续')

with draw_tab:
    # two text areas for inputing
    st.write('画图')
    pos_prompt = st.text_area('正向提示词', st.session_state.pos_prompt)
    neg_prompt = st.text_area('反向提示词', st.session_state.neg_prompt)

    if st.button('开始画图'):
        with st.spinner('Drawing...'):
            save_path = os.path.join(DEFAULT_DIR, f"{time.time()}.png")
            sd_default(pos_prompt, neg_prompt, save_path)
            st.image(save_path)

with modeling_tab:
    st.warning("TODO")