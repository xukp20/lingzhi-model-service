import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="3D模型贴图",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("3D模型贴图")
st.caption("前端暂不支持自动渲染生成图片，以下为Demo演示")

# Show demos
# 4 Rows, the first only a white 3d model
with st.container(border=True):
    st.caption("原始3D模型")
    components.html(
        """
        <iframe src="https://app.vectary.com/p/5RVjiV7k2ppDWEqx4DGkye" frameborder="0" width="100%" height="512"></iframe>
        """,
        height=512
    )

# the second, a pic and its rendered 3d model
with st.expander("示例1", expanded=True):
    with st.container(border=True, height=512):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image("https://img2.imgtp.com/2024/03/16/CpOWO3F7.png", width=512)
        with col2:
            components.html(
                """
                <iframe src="https://app.vectary.com/p/0DGRSjF5AKevy6Vg7LVP0m" frameborder="0" width="100%" height="512"></iframe>
                """,
                height=512
            )


# the third, a pic and its rendered 3d model
with st.expander("示例2", expanded=False):
    with st.container(border=True, height=512):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image("https://img2.imgtp.com/2024/03/16/qCZ0j79w.jpg", width=512)
        with col2:
            components.html(
                """
                <iframe src="https://app.vectary.com/p/5IlEIS4xeUT99FoG1QJGnH" frameborder="0" width="100%" height="512"></iframe>
                """,
                height=512
            )

