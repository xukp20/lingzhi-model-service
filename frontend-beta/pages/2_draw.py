import streamlit as st
import sys, os, time
sys.path.append(os.environ.get('PROJECT_BASE_DIR'))
from text2img.adapter import sd_default, save_encoded_image, get_model_names

# set pic saved path
DEFAULT_DIR = os.environ.get('PIC_CACHE_PATH')
if not os.path.exists(DEFAULT_DIR):
    os.makedirs(DEFAULT_DIR)

# set sessions
if st.session_state.get('pos_prompt') is None:
    st.session_state.pos_prompt = ''
    st.session_state.neg_prompt = ''

st.set_page_config(
    page_title="绘图",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# page elements
# two text areas for inputing
st.title('绘图')
# show select box for models
with st.expander('模型选择'):
    model_names = get_model_names()
    selected_model = st.selectbox('选择模型', model_names, label_visibility="collapsed")
    
if st.session_state.get('pos_prompt') == '':
    st.warning('请前往"需求转提示词页面"生成SD提示词')
    st.page_link('pages/1_prompt.py', label='前往需求转提示词页面', icon='🖊️')
else:
    st.toast('已获取到提示词', icon='😀')
    pos_prompt = st.text_area('正向提示词', st.session_state.pos_prompt)
    neg_prompt = st.text_area('反向提示词', st.session_state.neg_prompt)

    if st.button('开始画图'):
        with st.spinner('正在绘制...'):
            save_path = os.path.join(DEFAULT_DIR, f"{time.time()}.png")
            sd_default(pos_prompt, neg_prompt, save_path, use_model=selected_model)
            with st.container(border=True):
                st.image(save_path)

            # save the generated image path to session
            st.session_state.image_path = save_path

            st.toast('绘制成功，已保存图片', icon='😀')
            st.toast('选择贴图渲染或者转3D模型继续', icon='👇')
            col1, col2 = st.columns([1, 1])
            with col1:
                st.page_link('pages/3_render.py', label='前往渲染页面', icon='🎨')
            with col2:
                st.page_link('pages/4_pic2model.py', label='前往图片转3D页面', icon='🖼️')