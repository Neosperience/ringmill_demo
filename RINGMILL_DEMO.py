import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("RINGMILL DEMO")

st.sidebar.info("Select a demo above.")

st.markdown(
    """
    Demo.
"""
)