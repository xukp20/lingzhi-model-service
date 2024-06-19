import streamlit as st
import tempfile
from PIL import Image
# Import other required libraries
# load tripo project
import sys, os
import time
TRIPOSR_HOME = os.environ.get('TRIPOSR_HOME')
sys.path.append(TRIPOSR_HOME)
OBJ_CACHE_PATH = os.environ.get('OBJ_CACHE_PATH')
if not os.path.exists(OBJ_CACHE_PATH):
    os.makedirs(OBJ_CACHE_PATH)

st.set_page_config(
    page_title="图像转3D",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if st.session_state.get("image") is None:
    st.session_state.image = None

st.title("图像转3D")

with st.spinner("正在加载图片转3D模型..."):
    from interfaces import preprocess, generate


image = None
# Check if the image is given by the draw session
if st.session_state.get("image_path") is not None:
    image = Image.open(st.session_state.image_path)
    st.image(image, caption="Generated Image", width=128)
    st.caption("从绘图页面获取图片")
    st.session_state.image = image
else:
    # Upload input image
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.image = image

st.caption("可选以下示例图片")
path = os.path.join(TRIPOSR_HOME, "examples", "teapot.png")
demo_image = Image.open(path)
st.image(demo_image, caption="示例图片", width=128)
if st.button("使用示例图片"):
    image = demo_image
    st.session_state.image = image
    st.session_state.image_path = path


if st.session_state.image is not None:
    with st.expander("模型设置"):
        # Get user input
        remove_background = st.checkbox("Remove Background", value=True)
        foreground_ratio = st.slider("Foreground Ratio", 0.5, 1.0, 0.85, 0.05)
        mc_resolution = st.slider("Marching Cubes Resolution", 32, 320, 256, 32)

    # Preprocess image
    with st.spinner("正在预处理图像..."):
        preprocessed_image = preprocess(st.session_state.image, remove_background, foreground_ratio)

    # Display preprocessed image
    st.image(preprocessed_image, caption="预处理后图像", width=128)

    if st.button("生成模型"):
        # Generate 3D model
        # random name
        file_name = f"{time.time()}.glb"
        obj_path = os.path.join(OBJ_CACHE_PATH, file_name)
        with st.spinner("正在生成 3D 模型..."):
            generate(preprocessed_image, mc_resolution, obj_path, format="glb")

        st.toast("3D模型生成成功", icon="🎉")
        st.toast("暂不支持在线查看，点击下载查看", icon="👇")

        # download or clear
        st.download_button(
            label="下载",
            data=open(obj_path, "rb"),
            file_name=file_name,
            mime="model/gltf-binary",
        )
        if st.button("清除"):
            st.session_state.image = None
            st.session_state.image_path = None
            st.toast("生成结果已清除", icon="🗑️")
            st.rerun()

        # Render the 3D model
        ## Initialize pyvista reader and plotter
        # plotter = pv.Plotter(border=False, window_size=[500, 400])
        # plotter.background_color = "#f0f8ff"

        # ## Read the obj file
        # reader = pv.get_reader(obj_path)

        # ## Add the 3D model to the plotter
        # mesh = reader.read()
        # plotter.add_mesh(mesh, color="salmon")
        # plotter.view_isometric()

        # stpyvista(plotter, key="my_obj")

        