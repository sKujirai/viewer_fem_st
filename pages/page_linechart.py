import streamlit as st
import pandas as pd
import io
import os


def page_linechart():

    # Load DataFrame
    df = None

    file_buffer = st.file_uploader("Choose a CSV file", type='csv', encoding=None)

    csv_path = st.text_input('or input CSV file path', '')

    if file_buffer:
        uploaded_file = io.TextIOWrapper(file_buffer)
        if uploaded_file is not None:
            data_load_state = st.text('Loading data...')
            df = pd.read_csv(uploaded_file)
            data_load_state.text('Loading data...done')
    else:
        if os.path.isfile(csv_path):
            df = pd.read_csv(csv_path, encoding='utf-8')

    if df is not None:

        # Plot line chart
        index = st.sidebar.selectbox('Select index', df.columns)
        idx_val = list(df.columns)
        idx_val.remove(index)
        values = st.sidebar.multiselect('Select value', idx_val)
        values.append(index)

        if len(values) > 1:

            df_selected = df.loc[:, values]
            df_selected = df_selected.rename(columns={index: 'index'}).set_index('index')

            st.line_chart(df_selected)
