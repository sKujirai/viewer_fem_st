import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import re
import os
import time
import io

from pages.module.vtu_reader import VtkReader
from pages.module.draw_mesh import DrawMesh


def page_viewer():

    st.write('Viewer for VTK file in [XML format](https://vtk.org/Wiki/VTK_XML_Formats) (Unstructured grid)')

    base_dir = st.text_input('Input base dir', '.')

    file_buffer = st.file_uploader("or upload .vtu file", type=None, encoding=None)

    if file_buffer:
        content_byte = file_buffer.read()
        content_decoded = content_byte.decode('utf-8')
        file_path = './result.vtu'
        with open(file_path, mode='w') as f:
            f.write(content_decoded)
        files = []
        files.append(file_path)
    else:
        files = [f.name for f in os.scandir(base_dir) if re.search(r'\d+', f.name)]

        headers = list(set([re.sub(r'\d+$', '', f.rsplit('.')[0]) for f in files]))
        header = st.sidebar.selectbox('Select header', headers)

        files = [os.path.join(base_dir, f) for f in files if re.fullmatch(header, re.sub(r'\d+$', '', f.rsplit('.')[0])) is not None]
        files.sort(key=lambda s: int(re.search(r'\d+', s).group()))

    # VTK Reader
    reader = VtkReader()

    # Read first data
    try:
        reader.read(files[0])
    except Exception:
        st.error('Invalid file format')
        return
    data_dict = reader.get_data_dict()
    c0_xmin = np.min(reader.Coords[0, :])
    c0_xmax = np.max(reader.Coords[0, :])
    c0_ymin = np.min(reader.Coords[1, :])
    c0_ymax = np.max(reader.Coords[1, :])
    # Read last data
    reader.read(files[-1])
    cn_xmin = np.min(reader.Coords[0, :])
    cn_xmax = np.max(reader.Coords[0, :])
    cn_ymin = np.min(reader.Coords[1, :])
    cn_ymax = np.max(reader.Coords[1, :])
    # Set display area
    domain = {}
    domain['xmin'] = min(c0_xmin, cn_xmin)
    domain['xmax'] = max(c0_xmax, cn_xmax)
    domain['ymin'] = min(c0_ymin, cn_ymin)
    domain['ymax'] = max(c0_ymax, cn_ymax)
    len_x = domain['xmax'] - domain['xmin']
    len_y = domain['ymax'] - domain['ymin']
    domain['xmin'] -= 0.1 * len_x
    domain['xmax'] += 0.1 * len_x
    domain['ymin'] -= 0.1 * len_y
    domain['ymax'] += 0.1 * len_y
    domain['aspect'] = (domain['ymax'] - domain['ymin']) / (domain['xmax'] - domain['xmin'])

    # Get data list
    data_dict = reader.get_data_dict()

    # Get value list
    values = list(data_dict.keys())
    value = st.sidebar.selectbox('Select value', values)

    if value is not None:
        # Set system
        systems = [i + 1 for i in range(data_dict[value])]
        system = st.sidebar.selectbox('Select system', systems)

    display_mode = st.sidebar.selectbox('Select mode', ['Frame', 'Animation'])

    if display_mode == 'Frame':

        step = st.sidebar.number_input(
            f'Step No. 0 to {len(files) - 1}',
            min_value=0,
            max_value=len(files) - 1,
            value=0,
            step=1,
        )

        st.info('Value: {} System: {} Step: {}/{}'.format(value, system, step, len(files) - 1))

        reader.read(files[step])
        val = reader.get_value(value, system=system)

        drawer = DrawMesh()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        drawer.set_domain(ax, domain=domain)
        drawer.draw(coords=reader.Coords, connectivity=reader.Lnodes, value=val)

        st.pyplot(plt)

    elif display_mode == 'Animation':

        drawer = DrawMesh()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        drawer.set_domain(ax, domain=domain)

        latest_iteration = st.empty()
        bar = st.progress(0)

        stplot = st.pyplot(plt)

        def animate(istep):
            reader.read(files[istep])
            val = reader.get_value(value, system=system)
            drawer.draw(coords=reader.Coords, connectivity=reader.Lnodes, value=val)
            stplot.pyplot(plt)
            latest_iteration.text(f'Step: {istep}')
            bar.progress((istep + 1) / len(files))

        for istep in range(len(files)):
            animate(istep)
            time.sleep(0.005)
