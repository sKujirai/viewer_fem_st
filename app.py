import streamlit as st
# import ptvsd

from pages.page_viewer import page_viewer
from pages.page_linechart import page_linechart

pages = [
    'Overview',
    'Viewer',
    'LineChart',
]


def page_overview():
    st.info(
        """
        A simple web app to show results of FE analysis.\n
        Select a page in the upper left menu.
        """
    )


def select_page():

    page = st.sidebar.selectbox('Select page', pages)
    st.subheader(page)

    if page == 'Overview':
        page_overview()
    elif page == 'Viewer':
        page_viewer()
    elif page == 'LineChart':
        page_linechart()


if __name__ == '__main__':

    # ptvsd.enable_attach(address=('localhost', 5678))
    # ptvsd.wait_for_attach()  # Only include this line if you always wan't to attach the debugger

    select_page()
