import streamlit as st
import os
import time
# add the project base dir to the path
import sys
sys.path.append(os.environ.get('PROJECT_BASE_DIR'))
from llm.adapter import to_prompt, SYSTEM
from text2img.adapter import sd_default, save_encoded_image, get_model_names

DEFAULT_DIR = "./pics"
if not os.path.exists(DEFAULT_DIR):
    os.makedirs(DEFAULT_DIR)

# sessions
# record the pos_prompt and neg_prompt, triggered by the copy button
if 'pos_prompt' not in st.session_state:
    st.session_state.pos_prompt = ""
if 'neg_prompt' not in st.session_state:
    st.session_state.neg_prompt = ""
# record the system prompt
if 'system_prompt' not in st.session_state:
    st.session_state.system_prompt = SYSTEM

# three tabs
st.title('Lingzhi Model Service')
prompt_tab, draw_tab, modeling_tab = st.tabs(['Prompt', 'Draw', 'Modeling'])

with prompt_tab:
    st.write('需求转提示词')
    # add a expander for modifing the system prompt
    with st.expander('系统提示词'):
        # text area for inputing
        st.session_state.system_prompt = st.text_area('系统提示词', st.session_state.system_prompt, height=400, label_visibility="collapsed")
        # echo the system prompt as markdown
        st.caption('系统提示词 Markdown格式')
        st.markdown(st.session_state.system_prompt)


    input_col, button_col = st.columns([4, 1])
    with input_col:
        text_input = st.text_input('需求', '画一只猫', label_visibility="collapsed")
    with button_col:
        if text_input:
            start_button = st.button('开始转换')
    if start_button:
        with st.spinner('Generating...'):
            pos_prompt, neg_prompt = to_prompt(text_input, prompt=st.session_state.system_prompt)
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
    # show select box for models
    with st.expander('模型选择'):
        model_names = get_model_names()
        selected_model = st.selectbox('选择模型', list(model_names.keys()), label_visibility="collapsed")
        # if choose the first, then default and pass None
        selected_model = None if selected_model == list(model_names.keys())[0] else selected_model
        

    pos_prompt = st.text_area('正向提示词', st.session_state.pos_prompt)
    neg_prompt = st.text_area('反向提示词', st.session_state.neg_prompt)

    if st.button('开始画图'):
        with st.spinner('Drawing...'):
            save_path = os.path.join(DEFAULT_DIR, f"{time.time()}.png")
            sd_default(pos_prompt, neg_prompt, save_path, use_model=selected_model)
            st.image(save_path)

with modeling_tab:
    st.warning("TODO")