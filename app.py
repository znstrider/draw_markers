import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import matplotlib.pyplot as plt

update = st.button('Save')

st.text('1) Draw your markers in one stroke each')

markersize = st.sidebar.number_input('Choose a markersize', min_value=1, max_value=None, value=50)
linewidth = st.sidebar.number_input('Choose a marker linewidth', min_value=0., max_value=10., value=1., step=0.1)


# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=3,
    stroke_color="k",
    background_color="#eee",
    update_streamlit=update,
    height=150,
    drawing_mode="freedraw",
    key="canvas",
)
name_input = st.text_area('2) Name your markers seperated by a comma')

st.text('3) Save your markers by Clicking Save Above')


# Process the drawn data
if canvas_result.json_data is not None:
    marker_paths = []
    marker_names = name_input.split(',')
    marker_names = [name.strip() for name in marker_names]

    for d, name in zip(canvas_result.json_data["objects"], marker_names):
        path = d["path"]
        codes = [p[0] for p in path]
        vertices = np.array([p[-2:] for p in path])
        #normed = (vertices - vertices.mean(0)) / vertices.max(0)
        pt_ranges = vertices.max(0) - vertices.min(0)
        normed = (vertices - vertices.min(0) - 0.5*pt_ranges) / pt_ranges
        # flip vertically
        normed[:, 1] = normed[:, 1] * -1

        marker_paths.append(normed)
        np.savetxt(f'saved_paths/{name}.gz', normed)


# Example Plots of the drawn markers
if canvas_result.image_data is not None:
    n_markers = len(name_input.split(','))

    np.random.seed(442)
    _x = np.random.uniform(0,1,50)
    _y = np.random.uniform(0,1,50)

    fig, ax = plt.subplots(1, n_markers, figsize=(n_markers*4, 4))

    if not isinstance(ax, np.ndarray):
        ax = [ax]

    for ax_, path, marker_name in zip(ax, marker_paths, marker_names):
        ax_.set_facecolor('#eee')
        scatter = ax_.scatter(_x, _y, fc=fig.get_facecolor(), ec='C0', lw = linewidth,
                     marker=path,
                     s=markersize, zorder=999)
        ax_.set_title(marker_name)

    st.pyplot(fig)
